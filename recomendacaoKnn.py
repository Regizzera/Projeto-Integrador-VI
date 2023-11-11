import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors 

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

# Criando tabela pivot
filmes_pivot = avaliacoes_e_filmes.pivot_table(columns='ID_USUARIO', index='TITULO', values='AVALIACAO')
filmes_pivot.fillna(0, inplace=True)

# Transformando em matriz esparsa
filmes_sparse = csr_matrix(filmes_pivot)

# Criando modelo KNN
modelo = NearestNeighbors(n_neighbors=10, algorithm='brute')
modelo.fit(filmes_sparse)

def movie_recomendation(movie):
    recommendations = []
    distances, sugestions = modelo.kneighbors(filmes_pivot.filter(items=[movie], axis=0).values.reshape(1, -1))
    for i in range(len(sugestions[0])):
        title = filmes_pivot.index[sugestions[0][i]]
        recommendations.append(title)
    return recommendations
