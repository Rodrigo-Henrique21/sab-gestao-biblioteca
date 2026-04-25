# Gestão de Biblioteca

Sistema web para gestão de biblioteca com frontend responsivo e backend API em FastAPI.

## Estrutura de Pastas

```
.
├── src/
│   ├── app.py          # API FastAPI principal
│   ├── db.py           # Conexão com banco de dados
│   └── ...             # Outros módulos
├── static/
│   ├── css/
│   │   └── style.css   # Estilos CSS
│   └── js/
│       └── script.js   # JavaScript frontend
├── templates/
│   └── index.html      # Template HTML
├── tests/              # Testes
├── docs/               # Documentação
├── requirements.txt    # Dependências Python
├── schema.sql          # Schema do banco
├── seed.sql            # Dados iniciais
└── .env.example        # Exemplo de variáveis de ambiente
```

## Guia de Início Rápido

### 1. Configuração do Banco de Dados

#### Opção 1: Supabase (Recomendado)
1. Crie uma conta no [Supabase](https://supabase.com)
2. Crie um novo projeto
3. Vá para SQL Editor e execute o conteúdo de `schema.sql`
4. Execute o conteúdo de `seed.sql` para dados iniciais
5. Copie a connection string da aba Settings > Database

#### Opção 2: PostgreSQL Local
1. Instale PostgreSQL
2. Crie um banco de dados
3. Execute `schema.sql` e `seed.sql`

### 2. Configuração do Ambiente
1. Clone o repositório
2. Instale dependências: `pip install -r requirements.txt`
3. Copie `.env.example` para `.env`
4. Configure as variáveis:
   ```
   DATABASE_URL=postgresql://user:password@host:port/dbname
   SECRET_KEY=sua-chave-secreta-aqui
   ```

### 3. Executar Localmente
```bash
cd src
python app.py
# ou
uvicorn app:app --reload
```
Acesse http://localhost:8000

### 4. Deploy

#### Railway (Recomendado)
1. Crie conta no [Railway](https://railway.app)
2. Conecte seu repositório Git
3. Configure variáveis de ambiente no painel
4. Railway detectará automaticamente o projeto Python e fará deploy

#### Render
1. Crie conta no [Render](https://render.com)
2. Crie um novo Web Service
3. Conecte o repositório
4. Configure variáveis de ambiente:
   - `DATABASE_URL`
   - `SECRET_KEY`
5. Defina build command: `pip install -r requirements.txt`
6. Defina start command: `uvicorn src.app:app --host 0.0.0.0 --port $PORT`
7. Caso use deploy automático, o arquivo `render.yaml` já está incluído na raiz do projeto.

#### Github Pages (frontend apenas)
1. Faça deploy do frontend estático a partir da branch `main` ou `gh-pages`.
2. Publique o arquivo `index.html` na raiz do repositório e mantenha `static/` no mesmo nível.
3. Atualize `static/js/script.js` para usar a URL do backend hospedado no Render:
   ```js
   const API_BASE = 'https://SEU_BACKEND_AQUI';
   ```
4. Em GitHub Pages, o frontend será servido como site estático; todas as chamadas de API devem apontar para o backend remoto.

#### Outras Opções
- Heroku: Use buildpack Python
- Vercel: Para frontend estático, mas backend precisa de serverless

## Funcionalidades

- **Autenticação**: Login/cadastro com JWT
- **RBAC**: Usuário comum e Administrador
- **Livros**: CRUD completo, busca
- **Clientes**: Cadastro e listagem
- **Vendas**: Registro com controle de estoque
- **Dashboard**: Visões diferentes por role

## 🏦 Esquema de Banco de Dados (CockroachDB)

> Observação: CockroachDB é compatível com PostgreSQL; tipos e sintaxe seguem o padrão.  
> Habilite a extensão crypto se precisar de UUID:  
> `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`

```sql
CREATE TABLE IF NOT EXISTS livros (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo       STRING NOT NULL,
    autor        STRING NOT NULL,
    isbn         STRING UNIQUE NOT NULL,
    preco        DECIMAL(10,2) NOT NULL,
    estoque      INT NOT NULL CHECK (estoque >= 0),
    created_at   TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS clientes (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome         STRING NOT NULL,
    telefone     STRING,
    created_at   TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS vendas (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id   UUID NOT NULL REFERENCES clientes(id) ON DELETE RESTRICT,
    livro_id     UUID NOT NULL REFERENCES livros(id)   ON DELETE RESTRICT,
    quantidade   INT   NOT NULL CHECK (quantidade > 0),
    valor_total  DECIMAL(10,2) NOT NULL,
    created_at   TIMESTAMP DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_vendas_cliente ON vendas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_vendas_livro   ON vendas(livro_id);
```
## 📂 Estrutura do Repositório
```
sab-gestao-biblioteca/
├── src/
│   ├── db.py            # Conexão ao CockroachDB (SQLAlchemy + pooling)
│   ├── livros.py        # Regras de negócio de livros
│   ├── clientes.py      # Regras de negócio de clientes
│   ├── vendas.py        # Regras de negócio de vendas
│   ├── errors.py        # Exceções personalizadas
│   └── main.py          # CLI / orquestração
├── tests/
│   ├── test_livros.py
│   ├── test_clientes.py
│   └── test_vendas.py
├── docs/                # Documentação adicional
├── .github/workflows/ci.yml
├── requirements.txt
└── README.md
```
## 📐 Especificação Técnica por Módulo
- src/db.py
- Conexão segura ao CockroachDB Cloud
- Usa DATABASE_URL como string de conexão completa, idêntica à exibida no painel CockroachLabs (ex.: postgresql://rodrigo:<senha>@artful-elf-13228.j77.aws...).

```
"""
Gerencia a conexão com CockroachDB usando SQLAlchemy.
"""
import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")  # fornecida pelo provedor CockroachLabs
if not DATABASE_URL:
    raise RuntimeError("Variável de ambiente DATABASE_URL não definida.")

# echo=False desliga log de SQL; altere p/ True para debug
_ENGINE = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=0,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(bind=_ENGINE, expire_on_commit=False, future=True)

@contextmanager
def get_session():
    """Context manager que fornece sessão já com commit/rollback automático."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

## src/livros.py
- CRUD completo sobre tabela livros.

### Funções mínimas:

- cadastrar_livro(titulo, autor, isbn, preco, estoque) -> UUID
- listar_livros() -> List[Livro]
- buscar(titulo:str=None, autor:str=None, isbn:str=None) -> List[Livro]
- atualizar_estoque(isbn, delta:int)
- Regra: estoque nunca negativo; lançar EstoqueInsuficienteError.

## src/clientes.py
- CRUD sobre tabela clientes.

### Funções mínimas:

- cadastrar_cliente(nome, telefone) -> UUID
- listar_clientes() -> List[Cliente]
- obter_cliente_por_nome(nome) -> Cliente
- Regra: impedir duplicidade de nome + telefone.

## src/vendas.py
- Coordena transação que envolve cliente, livro e baixa de estoque.

### Funções mínimas:

- registrar_venda(nome_cliente, isbn, quantidade) -> UUID
- listar_vendas() -> List[Venda]
- relatorio_diario(data:date) -> Decimal
- 
### Regras:

- Tudo em uma transação: se falhar baixa de estoque, rollback.
- valor_total = livro.preco * quantidade no momento da venda.

## src/errors.py
### Classes de exceção:

* LivroJaExisteError
* LivroNaoEncontradoError
* ClienteJaExisteError
* ClienteNaoEncontradoError
* EstoqueInsuficienteError
* TransacaoErro
  
## src/main.py

```
1  – Cadastrar livro
2  – Listar livros
3  – Buscar livro
4  – Cadastrar cliente
5  – Listar clientes
6  – Registrar venda
7  – Relatório de vendas (hoje)
0  – Sair
Cada opção chama funções de negócio; main.py não contém SQL.
```

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
