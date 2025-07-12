import pytest
from src.livros import cadastrar_livro, buscar, atualizar_estoque
from src.errors import EstoqueInsuficienteError

def test_cadastrar_e_buscar():
    cadastrar_livro("Python", "Autor X", "ISBN1", 10.0, 5)
    resultado = buscar(isbn="ISBN1")[0]
    assert resultado[1] == "Python"   # 0-id, 1-titulo, 2-autor...

def test_atualizar_estoque():
    cadastrar_livro("Py", "X", "ISBN2", 10, 2)
    atualizar_estoque("ISBN2", -2)
    novo = buscar(isbn="ISBN2")[0]
    assert novo[5] == 0  # estoque é o sexto campo
    with pytest.raises(EstoqueInsuficienteError):
        atualizar_estoque("ISBN2", -1)
