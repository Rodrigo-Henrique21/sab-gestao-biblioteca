# src/clientes.py
from .db import get_cursor
from .errors import ClienteJaExisteError, ClienteNaoEncontradoError

def cadastrar_cliente(nome, telefone):
    try:
        with get_cursor(commit=True) as cur:
            cur.execute(
                """
                INSERT INTO clientes (nome, telefone)
                VALUES (%s, %s)
                """, (nome, telefone)
            )
    except Exception as e:
        if "duplicate key" in str(e):
            raise ClienteJaExisteError(f"Cliente {nome} ({telefone}) já existe.") from e
        raise

def listar_clientes():
    with get_cursor() as cur:
        cur.execute("SELECT id, nome, telefone FROM clientes ORDER BY nome")
        return cur.fetchall()

def obter_cliente_por_nome(nome):
    with get_cursor() as cur:
        cur.execute("SELECT id, nome, telefone FROM clientes WHERE nome = %s", (nome,))
        res = cur.fetchone()
        if not res:
            raise ClienteNaoEncontradoError(f"Cliente {nome} não encontrado.")
        return res
