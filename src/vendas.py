# src/vendas.py
from .db import get_cursor
from .clientes import obter_cliente_por_nome
from .livros import buscar, atualizar_estoque
from .errors import EstoqueInsuficienteError, TransacaoErro

def registrar_venda(nome_cliente, isbn, quantidade):
    try:
        cliente = obter_cliente_por_nome(nome_cliente)
        livro = buscar(isbn=isbn)
        if not livro:
            raise TransacaoErro("Livro não encontrado.")
        livro = livro[0]
        with get_cursor(commit=True) as cur:
            # Atualiza estoque
            cur.execute("SELECT estoque FROM livros WHERE isbn = %s FOR UPDATE", (isbn,))
            estoque_atual = cur.fetchone()
            if not estoque_atual:
                raise TransacaoErro("Livro não encontrado para atualizar estoque.")
            novo_estoque = estoque_atual[0] - quantidade
            if novo_estoque < 0:
                raise EstoqueInsuficienteError("Estoque insuficiente.")
            cur.execute("UPDATE livros SET estoque = %s WHERE isbn = %s", (novo_estoque, isbn))
            valor_total = float(livro[4]) * quantidade
            cur.execute(
                """
                INSERT INTO vendas (cliente_id, livro_id, quantidade, valor_total)
                VALUES (%s, %s, %s, %s)
                """,
                (cliente[0], livro[0], quantidade, valor_total)
            )
    except Exception:
        raise  # Deixe rolar para main.py tratar

def listar_vendas():
    with get_cursor() as cur:
        cur.execute("""
            SELECT v.id, c.nome, l.titulo, v.quantidade, v.valor_total, v.created_at
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN livros l ON v.livro_id = l.id
            ORDER BY v.created_at
        """)
        return cur.fetchall()

def relatorio_diario(data):
    with get_cursor() as cur:
        cur.execute("""
            SELECT COALESCE(SUM(valor_total), 0)
            FROM vendas
            WHERE DATE(created_at) = %s
        """, (data,))
        return cur.fetchone()[0]
