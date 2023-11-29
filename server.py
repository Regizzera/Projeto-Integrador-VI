from abc import ABC, abstractmethod
import socket
import threading
from RecomendacaoKnn import RecomendarFilme # Importa a classe RecomendarFilme

class Recomendador(ABC):
    @abstractmethod
    def filmes_recomendados(self, movie):
        pass
    
class GeradorRecomendacao:
    def __init__(self, recomendador):
        self.recomendador = recomendador
    """
        Classe responsável por gerar recomendações de filmes com base nos dados recebidos.

        Args:
        - movies: Uma lista de filmes para os quais as recomendações serão geradas.

        Returns:
        Um dicionário contendo recomendações para cada filme da lista.
        """
    def gerar_recomendacoes(self, movies):
        recomendacoes = {}
        for movie in movies:
            movie = movie.strip()
            recomendacoes[movie] = self.recomendador.filmes_recomendados(movie)
        return recomendacoes

class ClientHandler:
    def __init__(self, recomendador):
        self.recomendador = recomendador
        """
        Classe responsável por lidar com a lógica de comunicação com o cliente.

        Args:
        - client_socket: O socket do cliente conectado.

        Funciona recebendo os dados do cliente, gerando recomendações e enviando de volta ao cliente.
        """
    def handle(self, client_socket):
        try:
            # Recebe os dados do cliente
            data = client_socket.recv(1024)
            movies = data.decode("utf-8").split(',')
            print(f"Mensagem recebida: {movies}")

            # Gera as recomendações com base nos dados recebidos
            recommendation_generator = GeradorRecomendacao(self.recomendador)
            recomendacoes = recommendation_generator.gerar_recomendacoes(movies)
            print("Gerando recomendações:", recomendacoes)

            # Envia as recomendações de volta ao cliente
            client_socket.send(str(recomendacoes).encode("utf-8"))
        except Exception as e:
            print("[ERRO] Erro ao lidar com o cliente:", e)
        finally:
            client_socket.close()

class Servidor:
    def __init__(self, recomendador):
        self.recomendador = recomendador
        """
        Classe responsável por iniciar o servidor e gerenciar as conexões dos clientes.
        """
    def start(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind(('127.0.0.1', 12345))
        servidor.listen(5)
        print("[INFO] Servidor ouvindo na porta 12345...")

        try:
            while True:
                client, addr = servidor.accept()
                print("[INFO] Conexão aceita de {}:{}".format(addr[0], addr[1]))
                
                # Inicia uma nova thread para lidar com o cliente
                client_handler = threading.Thread(target=ClientHandler(self.recomendador).handle, args=(client,))
                client_handler.start()
        except KeyboardInterrupt:
            print("[INFO] Desligando o servidor.")
        finally:
            servidor.close()

# Exemplo de inicialização do Recomendador de Filmes
recomendador = RecomendarFilme() 
recomendador.carregar_dados('movies_metadata.csv', 'ratings.csv')
recomendador.treinar_modelo()

if __name__ == "__main__":
    servidor = Servidor(recomendador)
    servidor.start()
