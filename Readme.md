# API medfutura

Esta API permite criar, consultar, buscar, atualizar e excluir registros de pessoas em um banco de dados SQLite.

## Endpoints Disponiveis

- `POST /pessoas`: Cria uma nova pessoa.
- `GET /pessoas/:id`: Retorna os detalhes de uma pessoa.
- `GET /pessoas?t=:termo`: Busca pessoas por um termo.
- `PUT /pessoas/:id`: Atualiza as informações de uma pessoa.
- `DELETE /pessoas/:id`: Exclui uma pessoa.

## Como Rodar o Projeto

1. Clone o repositório e navegue até o diretório do projeto.
2. Crie e ative o ambiente virtual:
    ```sh
    python -m venv venv
    .venv\\Scripts\\activate
    ```
3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```
4. Crie o banco de dados:
    ```sh
    python initialize_sql.py
    ```
5. Configure as variáveis de ambiente no arquivo `.env`.
6. Inicie a aplicação:
    ```sh
    python app.py
    ```

## Tecnologias Utilizadas

- Python 3.12
- Flask
- SQLite

## Autor

Valdesmar
