import socket
import threading
from recomendacaoKnn import movie_recomendation

def handle_client(client_socket):
    try:
        data = client_socket.recv(1024)
        movies = data.decode("utf-8").split(',')

        recommendations = {}
        for movie in movies:
            movie = movie.strip()
            recommendations[movie] = movie_recomendation(movie)
        print("[INFO] Gerando recomendações:", recommendations)

        client_socket.send(str(recommendations).encode("utf-8"))
    except Exception as e:
        print("[ERRO] Erro ao lidar com o cliente:", e)
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 12345))
    server.listen(5)

    print("[INFO] Servidor ouvindo na porta 12345...")

    try:
        while True:
            client, addr = server.accept()
            print("[INFO] Conexão aceita de {}:{}".format(addr[0], addr[1]))
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start()
    except KeyboardInterrupt:
        print("[INFO] Desligando o servidor.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()