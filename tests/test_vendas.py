from datetime import date
from src.clientes import cadastrar_cliente
from src.livros import cadastrar_livro
from src.vendas import registrar_venda, relatorio_diario

def test_registrar_venda_e_relatorio():
    cadastrar_cliente("Carlos", "7777")
    cadastrar_livro("Livro", "Autor", "ISBN9", 20, 3)
    registrar_venda("Carlos", "ISBN9", 2)
    total = relatorio_diario(date.today())
    assert float(total) == 40.0
