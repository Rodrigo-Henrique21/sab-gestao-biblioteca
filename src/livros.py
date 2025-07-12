# src/livros.py
from .db import get_cursor
from .errors import LivroJaExisteError, LivroNaoEncontradoError, EstoqueInsuficienteError

def cadastrar_livro(titulo, autor, isbn, preco, estoque):
    try:
        with get_cursor(commit=True) as cur:
            cur.execute(
                """
                INSERT INTO livros (titulo, autor, isbn, preco, estoque)
                VALUES (%s, %s, %s, %s, %s)
                """, (titulo, autor, isbn, preco, estoque)
            )
    except Exception as e:
        if "duplicate key" in str(e):
            raise LivroJaExisteError(f"ISBN {isbn} já cadastrado.") from e
        raise

def listar_livros():
    with get_cursor() as cur:
        cur.execute("SELECT id, titulo, autor, isbn, preco, estoque FROM livros ORDER BY titulo")
        return cur.fetchall()

def buscar(isbn=None, titulo=None, autor=None):
    conds = []
    params = []
    if isbn:
        conds.append("isbn = %s")
        params.append(isbn)
    if titulo:
        conds.append("lower(titulo) LIKE lower(%s)")
        params.append(f"%{titulo}%")
    if autor:
        conds.append("lower(autor) LIKE lower(%s)")
        params.append(f"%{autor}%")
    where = " AND ".join(conds) if conds else "TRUE"
    with get_cursor() as cur:
        cur.execute(f"SELECT id, titulo, autor, isbn, preco, estoque FROM livros WHERE {where}", params)
        return cur.fetchall()

def atualizar_estoque(isbn, delta):
    with get_cursor(commit=True) as cur:
        cur.execute("SELECT estoque FROM livros WHERE isbn = %s FOR UPDATE", (isbn,))
        res = cur.fetchone()
        if not res:
            raise LivroNaoEncontradoError(f"Livro com ISBN {isbn} não encontrado.")
        novo_estoque = res[0] + delta
        if novo_estoque < 0:
            raise EstoqueInsuficienteError("Estoque insuficiente.")
        cur.execute("UPDATE livros SET estoque = %s WHERE isbn = %s", (novo_estoque, isbn))
