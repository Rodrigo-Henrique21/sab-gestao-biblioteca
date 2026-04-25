# Gestão de Biblioteca

Sistema web para gestão de biblioteca com frontend estático e backend em FastAPI.

## Visão geral

Este projeto reúne duas partes principais:

- **Frontend**: interface responsiva construída com HTML, CSS e JavaScript.
- **Backend**: API REST em Python usando FastAPI.
- **Banco de dados**: compatível com PostgreSQL/CockroachDB através de `DATABASE_URL`.

O frontend consome o backend via requisições AJAX e pode ser hospedado separadamente do servidor de API.

## Arquitetura

A arquitetura do projeto está disponível no arquivo `architecture.excalidraw`.

O diagrama mostra os principais serviços e fluxos:

- `GitHub Pages` para hospedar o frontend estático
- `Render` para executar o backend FastAPI
- `Supabase` como banco de dados PostgreSQL compatível
- Navegador do usuário acessando o frontend e consumindo a API

- `README.md`: documentação principal
- `architecture.excalidraw`: diagrama visual da arquitetura

## Frontend

O frontend é composto por:

- `templates/index.html` — página principal
- `static/css/style.css` — estilos e responsividade
- `static/js/script.js` — lógica de Fetch, formulários e renderização de dados

### Funcionalidades

- Exibe lista de livros e clientes
- Cadastro de livros
- Cadastro de clientes
- Registro de vendas e atualização de estoque
- Consumo de API para todas as operações

### Configuração da API

No arquivo `static/js/script.js`, existe uma constante com a URL base da API:

```js
const API_BASE = 'http://localhost:8000';
```

Para produção ou deploy separado, altere essa URL para apontar para o backend hospedado no Render ou outro serviço.

### Teste local do frontend

O frontend é estático e pode ser servido com um servidor simples:

```bash
cd c:\Users\FIC\Desktop\projetoSAP\sab-gestao-biblioteca-1
python -m http.server 8001
```

Acesse `http://localhost:8001` e verifique se as chamadas de API apontam para o backend correto.

## Backend

O backend usa FastAPI para expor endpoints que gerenciam:

- livros
- clientes
- vendas
- autenticação e autorização

Arquivos principais:

- `src/app.py` — aplicação FastAPI principal
- `src/db.py` — conexão com banco de dados
- `src/livros.py` — lógica de livros
- `src/clientes.py` — lógica de clientes
- `src/vendas.py` — lógica de vendas
- `src/errors.py` — exceções customizadas
- `src/main.py` — orquestração adicional e CLI

### Variáveis de ambiente

Copie o arquivo de exemplo e configure:

```powershell
copy .env.example .env
```

No `.env`, defina:

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=sua-chave-secreta-aqui
```

### Executando localmente

```bash
cd src
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

A API ficará disponível em `http://localhost:8000`.

## Deploy

### Backend no Render

1. Crie conta no [Render](https://render.com).
2. Crie um novo serviço do tipo **Web Service**.
3. Conecte o repositório Git.
4. Configure as variáveis de ambiente:
   - `DATABASE_URL`
   - `SECRET_KEY`
5. Build Command:

```bash
pip install -r requirements.txt
```

6. Start Command:

```bash
uvicorn src.app:app --host 0.0.0.0 --port $PORT
```

7. Mantenha o arquivo `render.yaml` na raiz para facilitar configurações de deploy.

### Frontend no GitHub Pages

O GitHub Pages serve apenas conteúdo estático.

1. Garanta que `templates/index.html` e a pasta `static/` estejam versionados no repositório.
2. No GitHub, abra as configurações do repositório.
3. Na seção **Pages**, escolha a branch `main` ou `gh-pages`.
4. Configure como `root` se o HTML estiver na raiz do repositório.
5. Atualize `static/js/script.js` para usar a URL pública do backend:

```js
const API_BASE = 'https://seu-backend.onrender.com';
```

6. Publique e teste.

### Uso combinado

- Backend: hospedado no Render
- Frontend: hospedado no GitHub Pages
- `API_BASE` deve apontar para a URL do backend

## Banco de dados

Use `sql/schema.sql` e `sql/seed.sql` para criar esquema e dados iniciais.

### Exemplo de conexão

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
```

## Estrutura do repositório

```text
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
├── render.yaml
├── README.md
├── .env.example
├── sql/
│   ├── schema.sql
│   └── seed.sql
└── scripts/
    └── teste_conectividade.py
```

## Funcionalidades principais

- Cadastro, edição e listagem de livros
- Cadastro e listagem de clientes
- Registro de vendas com controle de estoque
- Autenticação e autorização básica
- Interface web responsiva
- Possibilidade de deploy separado para frontend e backend

## Testes

Execute os testes com:

```bash
pytest
```

## Observações

- O backend pode ser executado localmente ou hospedado no Render.
- O frontend pode ser publicado no GitHub Pages ou servido junto com o backend.
- Se usar GitHub Pages, mantenha `API_BASE` atualizado para o backend remoto.
