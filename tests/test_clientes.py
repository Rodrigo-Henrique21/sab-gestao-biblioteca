import pytest
from src.clientes import cadastrar_cliente, obter_cliente_por_nome
from src.errors import ClienteJaExisteError

def test_cadastrar_cliente_unico():
    cadastrar_cliente("Ana", "9999")
    with pytest.raises(ClienteJaExisteError):
        cadastrar_cliente("Ana", "9999")

def test_obter_cliente():
    cadastrar_cliente("Bia", "8888")
    cli = obter_cliente_por_nome("Bia")
    assert cli[2] == "8888"   # telefone é o terceiro campo do select (id, nome, telefone)
