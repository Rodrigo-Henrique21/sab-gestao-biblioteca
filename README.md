
ajusteReadme.ipynb
ajusteReadme.ipynb_

[ ]
   1

Comece a programar ou gere código com IA.
## Projeto Final Python – Certificação PCAP (Exame PCAP-31-0x)

### 🎯 Contexto do Problema

Pequena livraria local que precisa de um sistema para gerenciar o catálogo de livros, clientes e realizar vendas de forma organizada. A solução deverá ter funcionalidades básicas de cadastro, pesquisa e controle de vendas, utilizando boas práticas de programação.

---

Projeto Final Python – Certificação PCAP (Exame PCAP-31-0x)
🎯 Contexto do Problema
Pequena livraria local que precisa de um sistema para gerenciar o catálogo de livros, clientes e realizar vendas de forma organizada. A solução deverá ter funcionalidades básicas de cadastro, pesquisa e controle de vendas, utilizando boas práticas de programação.

📋 Requisitos Funcionais
*

📌 Requisitos Não‑Funcionais
Código PEP‑8, com docstrings em todos os módulos/funções.
Tratamento robusto de exceções definidas em errors.py.
Persistência dos dados em CockroachDB (SQL) usando transações.
Testes unitários (>80 % de cobertura) em pytest.
CI no GitHub Actions executando testes a cada push.
🏦 Esquema de Banco de Dados (CockroachDB)
-- habilite a extensão crypto se precisar de UUID:  CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

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
Observação: CockroachDB é compatível com PostgreSQL; tipos e sintaxe seguem o padrão.

📂 Estrutura do Repositório
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
📐 Especificação Técnica por Módulo (instruções para dev contratado)
src/db.py
Conexão segura ao CockroachDB Cloud – usa DATABASE_URL como string de conexão completa, idêntica à que a CockroachLabs exibe no painel (ex.: postgresql://rodrigo:<senha>@artful-elf-13228.j77.aws-us-east-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full).

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
Teste rápido de conectividade (opcional)
"""quick_check.py"""
import os
import psycopg2

conn = psycopg2.connect(os.environ["DATABASE_URL"])
with conn.cursor() as cur:
    cur.execute("SELECT now()")
    print(cur.fetchone())
src/livros.py
CRUD completo sobre tabela livros.

Funções mínimas:

cadastrar_livro(titulo, autor, isbn, preco, estoque) -> UUID
listar_livros() -> List[Livro]
buscar(titulo:str=None, autor:str=None, isbn:str=None) -> List[Livro]
atualizar_estoque(isbn, delta:int)
Regra: estoque nunca negativo; lançar EstoqueInsuficienteError.

src/clientes.py
CRUD sobre tabela clientes.

Funções mínimas:

cadastrar_cliente(nome, telefone) -> UUID
listar_clientes() -> List[Cliente]
obter_cliente_por_nome(nome) -> Cliente
Regra: impedir duplicidade de nome + telefone.

src/vendas.py
Coordena transação que envolve cliente, livro e baixa de estoque.

Funções mínimas:

registrar_venda(nome_cliente, isbn, quantidade) -> UUID
listar_vendas() -> List[Venda]
relatorio_diario(data:date) -> Decimal
Regras:

Tudo em uma transação: se falhar baixa de estoque, rollback.
valor_total = livro.preco * quantidade no momento da venda.
src/errors.py
Classes de exceção: LivroJaExisteError, LivroNaoEncontradoError, ClienteJaExisteError, ClienteNaoEncontradoError, EstoqueInsuficienteError, TransacaoErro.

src/main.py
Menu CLI textual:

1  – Cadastrar livro
2  – Listar livros
3  – Buscar livro
4  – Cadastrar cliente
5  – Listar clientes
6  – Registrar venda
7  – Relatório de vendas (hoje)
0  – Sair
Cada opção chama funções de negócio; main.py não contém SQL.

🚀 Roadmap (GitHub Projects revisado)
#	Cartão	Descrição	Estimativa
1	Setup repositório	Pastas, requirements, linters	0.5 h
2	Conexão DB	Implementar db.py com SQLAlchemy	0.8 h
3	Tabelas SQL	Rodar script schema.sql no Cockroach	0.3 h
4	Módulo livros	CRUD + testes	1.2 h
5	Módulo clientes	CRUD + testes	1 h
6	Módulo vendas	Transação + relatório + testes	1.5 h
7	CLI	main.py menu e validações	1 h
8	CI GitHub	Workflow pytest + coverage badge	0.5 h
9	Documentação	Atualizar README, diagramas	0.5 h
Produtos pagos do Colab - Cancelar contratos
