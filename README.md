# Gestão de Biblioteca

Projeto de gestão de biblioteca com frontend estático e backend em FastAPI.

## Visão Geral do Projeto

Este repositório reúne duas partes principais:

1. **Frontend**: interface web leve construída com HTML, CSS e JavaScript, que roda como aplicação estática.
2. **Backend**: API REST em FastAPI para gerenciar livros, clientes, vendas e autenticação.
3. **Banco de dados**: compatível com PostgreSQL / CockroachDB, usando `DATABASE_URL` para conexão.

O frontend consome o backend via chamadas AJAX e pode ser hospedado separadamente do servidor de API.

## Frontend

O frontend é construído com arquivos estáticos:

- `templates/index.html` — página principal do sistema
- `static/css/style.css` — estilos responsivos
- `static/js/script.js` — lógica de consumo da API, envio de formulários e renderização de dados

### O que o frontend faz

- Exibe lista de livros e clientes
- Permite cadastro de livros e clientes
- Registra vendas e atualiza estoque
- Chama o backend para todas as operações de CRUD

### Como o frontend se conecta ao backend

No arquivo `static/js/script.js`, existe uma constante para a URL base da API:

```js
const API_BASE = 'http://localhost:8000';
```

Para deploy no GitHub Pages, essa URL deve apontar para o serviço do backend hospedado no Render ou outro provider.

## Backend

O backend é uma API Python usando FastAPI. Ele expõe endpoints para:

- livros
- clientes
- vendas
- autenticação e autorização

Arquivos principais:

- `src/app.py` — aplicação FastAPI principal
- `src/db.py` — conexão com banco de dados
- `src/livros.py` — regras de negócio dos livros
- `src/clientes.py` — regras de negócio dos clientes
- `src/vendas.py` — regras de negócio de vendas
- `src/errors.py` — exceções personalizadas
- `src/main.py` — orquestração / ponto de entrada adicional

### Principais regras do backend

- Controle de estoque para vendas
- Transações consistentes ao registrar venda
- Validação de dados e tratamento de erros
- Possibilidade de separar autenticação via JWT

## Instalação Local

### Pré-requisitos

- Python 3.10+ instalado
- PostgreSQL ou outro banco compatível
- Virtualenv recomendado

### Passos

```bash
python -m venv env
env\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Variáveis de ambiente

Copie o arquivo de exemplo:

```powershell
copy .env.example .env
```

Configure no `.env` as variáveis:

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=sua-chave-secreta-aqui
```

### Executar localmente

```bash
cd src
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Acesse `http://localhost:8000` para o backend. Se o frontend estiver servido pela própria API, o `index.html` deverá estar disponível.

## Deploy

### Deploy do Backend no Render

1. Crie conta no [Render](https://render.com).
2. Crie um novo serviço do tipo **Web Service**.
3. Conecte seu repositório Git.
4. Configure as variáveis de ambiente:
   - `DATABASE_URL`
   - `SECRET_KEY`
5. Build Command:
   ```bash
   pip install -r requirements.txt
   ```
6. Start Command:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port $PORT
   ```
7. Mantenha o arquivo `render.yaml` na raiz para facilitar deploy automático e configurações de service.

> No Render, o backend receberá uma URL pública. Use essa URL para o frontend estático.

### Deploy do Frontend no GitHub Pages

O GitHub Pages só serve arquivos estáticos, então aqui hospedamos apenas o frontend.

1. Faça commit de `templates/index.html` e `static/` no repositório.
2. No GitHub, ative o GitHub Pages apontando para a branch `main` ou `gh-pages`.
3. Garanta que `index.html` e `static/` estejam no mesmo nível a partir da raiz do site.
4. Ajuste `static/js/script.js` para usar a URL do backend hospedado no Render:

```js
const API_BASE = 'https://seu-backend.onrender.com';
```

5. Publique e teste a aplicação estática.

> Importante: GitHub Pages não executa Python. Todas as operações de dados continuarão a depender do backend remoto.

### Como usar Render + GitHub Pages juntos

- Backend: `https://seu-backend.onrender.com` no Render
- Frontend: GitHub Pages serve `index.html`
- Atualize a variável `API_BASE` para a URL do backend
- O frontend estático faz requisições AJAX ao backend remoto

## Estrutura do Projeto

```
.
├── src/
│   ├── app.py
│   ├── db.py
│   ├── livros.py
│   ├── clientes.py
│   ├── vendas.py
│   ├── errors.py
│   └── main.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── tests/
│   ├── test_clientes.py
│   ├── test_livros.py
│   └── test_vendas.py
├── requirements.txt
├── schema.sql
├── seed.sql
├── render.yaml
└── README.md
```

## Funcionalidades Principais

- Cadastro, edição e listagem de livros
- Cadastro e listagem de clientes
- Registro de vendas com atualização de estoque
- Autenticação e autorização básica
- Interface responsiva para uso no navegador
- Possibilidade de deploy separado para frontend e backend

## Banco de Dados

Use `schema.sql` e `seed.sql` para criar o esquema e dados iniciais.

### Exemplo de conexão compatível

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
```

## Observações

- O backend pode ser executado localmente ou hospedado no Render.
- O frontend pode ser servido diretamente pelo backend ou publicado como site estático no GitHub Pages.
- Se optar por GitHub Pages, mantenha a URL da API atualizada em `static/js/script.js`.

## Testes

Para executar os testes:

```bash
pytest
```

---

Se quiser, posso também adicionar um exemplo de `render.yaml` e um guia passo a passo para criar a branch `gh-pages` no GitHub.

## 🚀 Roadmap (GitHub Projects revisado)
| #  | Cartão            | Descrição                            | Estimativa |
|----|-------------------|--------------------------------------|------------|
| 1  | Setup repositório | Pastas, requirements, linters        | 0.5 h      |
| 2  | Conexão DB        | Implementar db.py com SQLAlchemy     | 0.8 h      |
| 3  | Tabelas SQL       | Rodar script schema.sql no Cockroach | 0.3 h      |
| 4  | Módulo livros     | CRUD + testes                        | 1.2 h      |
| 5  | Módulo clientes   | CRUD + testes                        | 1 h        |
| 6  | Módulo vendas     | Transação + relatório + testes       | 1.5 h      |
| 7  | CLI               | main.py menu e validações            | 1 h        |
| 8  | CI GitHub         | Workflow pytest + coverage badge     | 0.5 h      |
| 9  | Documentação      | Atualizar README, diagramas          | 0.5 h      |
