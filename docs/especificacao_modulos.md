`src/db.py`

**Responsável**: abre/fecha conexões e fornecer Session (SQLAlchemy).

**Requisitos**:

* Função `get_session()` retornando context‑manager.
* Pool mínimo de 5 conexões.
* Credenciais lidas de variáveis ambiente (`COCKROACH_URI`).

`src/livros.py`

CRUD completo sobre tabela `livros`.

**Funções mínimas**:

* `cadastrar_livro(titulo, autor, isbn, preco, estoque)` -> `UUID`
* `listar_livros()` -> `List[Livro]`
* `buscar(titulo:str=None, autor:str=None, isbn:str=None)` -> `List[Livro]`
* `atualizar_estoque(isbn, delta:int)`

**Regra**: estoque nunca negativo; lança `EstoqueInsuficienteError`.

`src/clientes.py`

CRUD sobre tabela `clientes`.

**Funções mínimas**:

* `cadastrar_cliente(nome, telefone)` -> `UUID`
* `listar_clientes()` -> `List[Cliente]`
* `obter_cliente_por_nome(nome)` -> `Cliente`

**Regra**: impedi duplicidade de nome + telefone.

`src/vendas.py`

Coordena transação que envolve cliente, livro e baixa de estoque.

**Funções mínimas**:

* `registrar_venda(nome_cliente, isbn, quantidade)` -> `UUID`
* `listar_vendas()` -> `List[Venda]`
* `relatorio_diario(data:date)` -> `Decimal`

**Regras**:

* Tudo em uma transação: se falhar baixa de estoque, rollback.
* `valor_total = livro.preco * quantidade` no momento da venda.

`src/errors.py`

Classes de exceção: `LivroJaExisteError`, `LivroNaoEncontradoError`, `ClienteJaExisteError`, `ClienteNaoEncontradoError`, `EstoqueInsuficienteError`, `TransacaoErro`.

`src/main.py`

Menu CLI textual:

1  – Cadastrar livro
2  – Listar livros
3  – Buscar livro
4  – Cadastrar cliente
5  – Listar clientes
6  – Registrar venda
7  – Relatório de vendas (hoje)
0  – Sair

Cada opção chama funções de negócio; `main.py` não contém SQL.