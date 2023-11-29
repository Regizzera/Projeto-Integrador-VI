import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

class RecomendarFilme:
    def __init__(self):
        self.model = None
        self.filmes_pivot = None
        self.filmes_sparse = None

    def carregar_dados(self, movies_file, ratings_file):
        # Carregando os dados
        filmes = pd.read_csv('movies_metadata.csv', low_memory=False)
        avaliacoes = pd.read_csv('ratings.csv')

        # Filtrando e renomeando colunas
        filmes = filmes[['id', 'original_title', 'original_language', 'vote_count']]
        filmes.rename(columns={'id': 'ID_FILME', 'original_title': 'TITULO', 'original_language': 'LINGUAGEM', 'vote_count': 'QT_AVALIACOES'}, inplace=True)

        avaliacoes = avaliacoes[['userId', 'movieId', 'rating']]
        avaliacoes.rename(columns={'userId': 'ID_USUARIO', 'movieId': 'ID_FILME', 'rating': 'AVALIACAO'}, inplace=True)

        # Removendo valores nulos
        filmes.dropna(inplace=True)

        # Filtrando usuários com mais de 999 avaliações
        qt_avaliacoes = avaliacoes['ID_USUARIO'].value_counts() > 999
        y = qt_avaliacoes[qt_avaliacoes].index
        avaliacoes = avaliacoes[avaliacoes['ID_USUARIO'].isin(y)]

        # Filtrando filmes com mais de 999 avaliações
        filmes = filmes[filmes['QT_AVALIACOES'] > 999]

        # Filtrando filmes em inglês
        filmes = filmes[filmes['LINGUAGEM'] == 'en']

        # Convertendo ID_FILME para inteiro
        filmes['ID_FILME'] = filmes['ID_FILME'].astype(int)

        # Concatenando os dataframes
        avaliacoes_e_filmes = avaliacoes.merge(filmes, on='ID_FILME')

        # Removendo duplicatas
        avaliacoes_e_filmes.drop_duplicates(['ID_USUARIO', 'ID_FILME'], inplace=True)
        del avaliacoes_e_filmes['ID_FILME']

        # Transformar em matriz esparsa e atribuir a self.filmes_sparse
        self.filmes_pivot = avaliacoes_e_filmes.pivot_table(columns='ID_USUARIO', index='TITULO', values='AVALIACAO')
        self.filmes_pivot.fillna(0, inplace=True)
        self.filmes_sparse = csr_matrix(self.filmes_pivot)

    def treinar_modelo(self):
        if self.filmes_sparse is None:
            raise ValueError("Dados não carregados. Execute 'carregar_dados()' antes de treinar o modelo.")
        
        # Criação do modelo se ainda não foi criado
        if self.model is None:
            self.model = NearestNeighbors(n_neighbors=10, algorithm='brute')
            self.model.fit(self.filmes_sparse)
 
    def filmes_recomendados(self, movie):
        # Garante que o título do filme esteja no mesmo formato (minúsculas)
        movie = movie.lower()

        # Verifica se os dados estão carregados
        if self.filmes_sparse is None:
            raise ValueError("Dados não carregados. Execute 'carregar_dados()' antes de gerar recomendações.")

        # Garante que todos os títulos na tabela pivot estejam no mesmo formato (minúsculas)
        filmes_pivot_lower = self.filmes_pivot.index.str.lower()

        # Verifica se o filme está na lista de filmes (em minúsculas)
        if movie not in filmes_pivot_lower:
            raise ValueError(f"O filme '{movie}' não foi encontrado na base de dados.")

        # Obtém o índice do filme correspondente na tabela pivot
        movie_index = filmes_pivot_lower.get_loc(movie)

        # Obtém recomendações para o filme
        recomendacoes = []
        distances, sugestions = self.model.kneighbors(self.filmes_pivot.iloc[movie_index].values.reshape(1, -1))
        for i in range(len(sugestions[0])):
            title = self.filmes_pivot.index[sugestions[0][i]]
            recomendacoes.append(title)
        return recomendacoes
