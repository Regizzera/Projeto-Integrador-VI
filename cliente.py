import tkinter as tk
from tkinter import ttk
import socket

def communicate_with_server(filmes_usuario):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 12345))

        print(f"Enviando mensagem: {filmes_usuario}")
        client_socket.send(filmes_usuario.encode("utf-8"))

        response = client_socket.recv(4096)
        recommendations = eval(response.decode("utf-8"))

        print("Mensagem recebida:", recommendations)
        client_socket.close()

        return recommendations
    except Exception as e:
        print("[ERRO] Erro na comunicação com o servidor:", e)
        return None

def show_recommendations(entry_text, listbox):
    print("Usuário clicou em obter recomendações")
    filmes_usuario = entry_text.get()
    filmes_usuario = filmes_usuario.split(',')

    listbox.delete(0, tk.END)

    for movie in filmes_usuario:
        recommendations = communicate_with_server(movie)
        if recommendations is not None:
            listbox.insert(tk.END, f"Para o filme '{movie}', as recomendações são:")
            for idx, title in enumerate(recommendations):
                listbox.insert(tk.END, f"Opção {idx} - {title}")
        else:
            listbox.insert(tk.END, f"Erro ao obter recomendações para o filme '{movie}'")

def get_user_input():
    root = tk.Tk()
    root.title("Recomendação de Filmes")

    label = ttk.Label(root, text="Digite o nome dos filmes separados por vírgula:")
    label.pack(pady=10)

    entry = ttk.Entry(root, width=40)
    entry.pack(pady=10)

    button = ttk.Button(root, text="Obter Recomendações", command=lambda: show_recommendations(entry, listbox))
    button.pack(pady=10)

    listbox = tk.Listbox(root, width=60)
    listbox.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    get_user_input()
