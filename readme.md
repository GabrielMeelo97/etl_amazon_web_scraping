# Coleta de dados da Amazon e inserção no banco Postgres

Este código tem como objetivo coletar informações de livros da Amazon, incluindo nome, pontuação, classificações e avaliações, e inserir esses dados em um banco de dados Postgres.

## Configurações

O arquivo `constantes.py` contém as configurações necessárias para executar o código. Nele, você pode configurar o nome de páginas, configurações de login no banco e a palavra chave de busca na Amazon.

## Requisitos

Para executar este projeto, você precisa ter instalado:

- Python 3
- Bibliotecas Python
- Docker
- Docker Compose

Para instalar as bibliotecas, basta executar o seguinte comando no terminal:
```bash
pip install -r requirements.txt
```

## Utilização

1. Clone o repositório em sua máquina local.
2. Configure as variáveis de ambiente no arquivo `constantes.py` de acordo com suas necessidades.
3. Execute o arquivo `app.py` utilizando o seguinte comando no terminal:
```bash
python app.py
```

Isso iniciará a coleta de dados e a inserção no banco Postgres. Os dados serão salvos na tabela `scrapping_amazon`.

## Banco de dados

O arquivo `docker-compose.yml` contém a configuração para criar um banco de dados Postgres utilizando Docker. Para executar o banco de dados, execute o seguinte comando no terminal:
```bash
docker-compose up -d
```

Este comando iniciará o container do banco de dados. O banco de dados será criado automaticamente quando o código for executado.
