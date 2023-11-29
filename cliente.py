import tkinter as tk
from tkinter import ttk, messagebox
import socket
from typing import List, Dict, Union
import pandas as pd

class ServiçoRecomendaçãoFilmes:
    def comunicacao_com_servidor(self, movie: str) -> Union[None, Dict[str, List[str]]]:
        """Envia o nome do filme para o servidor e recebe recomendações."""
        try:
            # Estabelece conexão com o servidor
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', 12345))

            # Envia o nome do filme ao servidor
            print(f"Enviando mensagem: {movie}")
            client_socket.send(movie.encode("utf-8"))

            # Recebe a resposta do servidor
            response = client_socket.recv(4096)
            recomendacoes = eval(response.decode("utf-8"))

            # Imprime os filmes recomendados pelo servidor
            for movie, filmes_recomendados in recomendacoes.items():
                print(f"Mensagem recebida: Para o filme '{movie}', as recomendações são: {filmes_recomendados}")

            # Fecha a conexão com o servidor
            client_socket.close()

            return recomendacoes
        except Exception as e:
            print("[ERRO] Erro na comunicação com o servidor:", e)
            return None

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Recomendação de Filmes")
        self.movie_info_cache = {}
        self.create_widgets()
        self.entry.bind('<Return>', self.exibir_recomendacoes)

    def create_widgets(self):
        # Elementos da interface gráfica
        label = ttk.Label(self.root, text="Digite o nome dos filmes separados por vírgula:")
        label.pack(pady=10)

        self.entry = ttk.Entry(self.root, width=40)
        self.entry.pack(pady=10)

        button = ttk.Button(self.root, text="Obter Recomendações", command=self.exibir_recomendacoes)
        button.pack(pady=10)

        self.listbox = tk.Listbox(self.root, width=60)
        self.listbox.pack(pady=10)
        # Adiciona um evento para capturar a tecla "Enter" na listbox
        self.listbox.bind("<Return>", self.pressionar_enter)
        
        self.movie_service = ServiçoRecomendaçãoFilmes()  # Instância do serviço de recomendação

    def exibir_recomendacoes(self, event=None):
        # Filmes digitados pelo usuário
        filmes_usuario = self.entry.get()
        filmes_usuario = filmes_usuario.split(',')

        # Limpa a caixa de listagem
        self.listbox.delete(0, tk.END)

        # Para cada filme digitado, obtém as recomendações do servidor e exibe na interface
        for movie in filmes_usuario:
            recomendacoes = self.movie_service.comunicacao_com_servidor(movie)
            self.listbox.insert(tk.END, f"Para o filme '{movie}', as recomendações são:")

            if recomendacoes is not None and movie in recomendacoes:
                for idx, title in enumerate(recomendacoes[movie]):
                    self.listbox.insert(tk.END, f"- {title}")
            else:
                self.listbox.insert(tk.END, "Nenhuma recomendação encontrada para este filme.")

    def get_movie_info(self, movie):
        # Verifica se as informações já estão em cache
        if movie in self.movie_info_cache:
            return self.movie_info_cache[movie]

        # Carrega o conjunto de dados
        dataset = pd.read_csv('movies_metadata.csv', low_memory=False)

        # Encontra o filme no dataset (removendo espaços em branco e convertendo para minúsculas)
        movie = movie.lower().strip()
        movie_entry = dataset[dataset['original_title'].str.lower().str.strip() == movie]

        if len(movie_entry) == 0:
            return "Informações não encontradas"

        # Extrai os gêneros do filme
        genres_str = movie_entry['genres'].values[0]
        genres = eval(genres_str) if pd.notnull(genres_str) else []
        genre_names = [genre['name'] for genre in genres]

        # Obtém a sinopse do filme
        overview = movie_entry['overview'].values[0]

        # Armazena as informações em cache
        movie_info = f"Gênero: {', '.join(genre_names)}\nSinopse: {overview}"
        self.movie_info_cache[movie] = movie_info

        return movie_info

    def selecionar_filme(self, event):
        # Obtém o filme selecionado
        selected_movie = self.listbox.get(tk.ACTIVE)
        movie_name = selected_movie[2:]
        movie_info = self.get_movie_info(selected_movie[2:])  # Remove o traço inicial

        # Exibe as informações em uma janela de mensagem
        tk.messagebox.showinfo(f"Informações do Filme - {movie_name}", movie_info)

    def pressionar_enter(self, event):
        # Chama a função de exibição de informações quando "Enter" é pressionado
        self.selecionar_filme(event)

def get_user_input():
    # Cria a janela principal da interface gráfica
    janela = tk.Tk()
    app = GUI(janela)
    janela.mainloop()

if __name__ == "__main__":
    get_user_input()
