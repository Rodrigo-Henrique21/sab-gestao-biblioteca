# Backend — Gestão de Biblioteca

Este documento descreve a parte de backend do projeto.

## Visão geral

O backend é uma API REST construída com FastAPI e Python.
Ele gerencia as entidades do sistema, como livros, clientes e vendas, e oferece endpoints para o frontend consumir.

## Arquivos principais

- `src/app.py` — aplicação FastAPI principal
- `src/db.py` — conexão com o banco de dados
- `src/livros.py` — regras de negócio e operações sobre livros
- `src/clientes.py` — regras de negócio e operações sobre clientes
- `src/vendas.py` — regras de negócio e operações sobre vendas
- `src/errors.py` — exceções personalizadas
- `src/main.py` — orquestração e ponto de entrada adicional

## Principais responsabilidades

- gerenciamento de livros (CRUD)
- cadastro e listagem de clientes
- registro de vendas com controle de estoque
- transações consistentes para operações de venda
- tratamento de erros e validação de dados

## Dependências

As dependências estão em `requirements.txt`.

## Variáveis de ambiente

O backend depende de:

- `DATABASE_URL` — string de conexão com o banco de dados PostgreSQL/CockroachDB
- `SECRET_KEY` — chave secreta para segurança e assinatura de tokens, se usada

## Configuração local

1. Crie e ative um ambiente virtual:

```powershell
python -m venv env
env\Scripts\Activate.ps1
```

2. Instale as dependências:

```powershell
pip install -r requirements.txt
```

3. Configure o arquivo `.env` com as variáveis necessárias.

## Executando localmente

```powershell
cd src
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

A API ficará disponível em `http://localhost:8000`.

## Testes

Execute todos os testes com:

```powershell
pytest
```

## Observações

- O backend pode ser executado independentemente do frontend.
- Em produção, a API deve estar disponível por uma URL pública para o frontend estático se conectar.
- O backend também pode servir arquivos estáticos se configurado para isso, mas neste projeto o frontend é tipicamente hospedado separadamente.
