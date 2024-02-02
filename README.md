# Sistema de Recomendação de Filmes

Este é um projeto de sistema de recomendação de filmes baseado em filtragem colaborativa usando o algoritmo KNN e a arquitetura cliente-servidor. O servidor fornece recomendações com base na lista de filmes fornecida pelos clientes.	

**Funcionalidades:**

Recomendações Personalizadas: Receba recomendações de filmes personalizadas com base na sua lista de filmes favoritos usando o algoritmo KNN.

Comunicação via TCP: A comunicação entre o cliente e o servidor é realizada usando o protocolo TCP para garantir a entrega confiável e ordenada de dados.

**Nomes dos Arquivos:**

servidor.py: Código para iniciar o servidor.

cliente.py: Código para a interface de linha de comando do cliente.

recomendacaoKnn.py: Implementação do algoritmo KNN para recomendações.

**Pré-requisitos**

Python 3.x instalado

Bibliotecas Python necessárias (veja requirements.txt)

**Instalação e Execução**

Clone este repositório:

git clone https://github.com/seu-usuario/sistema-recomendacao-filmes.git

Navegue até o diretório do projeto:

cd sistema-recomendacao-filmes

Instale as dependências:
pip install -r requirements.txt

Inicie o servidor:

python servidor.py

Execute o cliente:

python cliente.py

Insira os nomes dos filmes na interface do cliente e pressione "Obter Recomendações".

**Contribuindo**

Sinta-se à vontade para abrir issues relatando problemas ou sugerindo melhorias.
Contribuições por meio de pull requests são bem-vindas.
