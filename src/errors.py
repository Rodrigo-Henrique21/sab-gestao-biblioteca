"""
Módulo de exceções customizadas do sistema da livraria.
Cada exceção representa um erro de negócio, facilitando a manutenção e o tratamento na interface (main.py).

Sempre que detectar uma situação de erro prevista em regra de negócio,
lançar a exceção correspondente.
"""

class LivroJaExisteError(Exception):
    """
    Erro para tentativa de cadastro de livro com ISBN já existente.

    Exemplo:
        raise LivroJaExisteError("Livro com ISBN 978... já cadastrado.")

    Possíveis causas:
        - Cadastro de novo livro com ISBN já registrado.
        - Tentativa de importar lote contendo ISBNs duplicados.
    """
    pass

class LivroNaoEncontradoError(Exception):
    """
    Erro para tentativa de acesso a livro inexistente (por ISBN ou id).

    Exemplo:
        raise LivroNaoEncontradoError("Livro com ISBN 978... não encontrado.")

    Possíveis causas:
        - Busca, alteração ou remoção de livro por ISBN inexistente.
        - Tentativa de registrar venda de livro não cadastrado.
    """
    pass

class ClienteJaExisteError(Exception):
    """
    Erro para tentativa de cadastro de cliente já registrado (mesmo nome + telefone).

    Exemplo:
        raise ClienteJaExisteError("Cliente André Ramos (11999990001) já existe.")

    Possíveis causas:
        - Cadastro manual de cliente já existente.
        - Tentativa de importar lote de clientes duplicados.
    """
    pass

class ClienteNaoEncontradoError(Exception):
    """
    Erro para operações em cliente não cadastrado.

    Exemplo:
        raise ClienteNaoEncontradoError("Cliente Beatriz Souza não encontrado.")

    Possíveis causas:
        - Venda para cliente não registrado.
        - Busca, alteração ou remoção de cliente inexistente.
    """
    pass

class EstoqueInsuficienteError(Exception):
    """
    Erro para tentativa de venda/baixa de estoque maior que o disponível.

    Exemplo:
        raise EstoqueInsuficienteError("Estoque insuficiente para ISBN 978...")

    Possíveis causas:
        - Registro de venda acima do estoque atual.
        - Baixa manual de estoque para valor negativo.
    """
    pass

class TransacaoErro(Exception):
    """
    Erro genérico para falha em operações atômicas (como registrar venda).
    Use para casos não previstos acima ou erro inesperado em uma transação.

    Exemplo:
        raise TransacaoErro("Falha ao registrar venda devido a erro de conexão.")

    Possíveis causas:
        - Falha de comunicação com o banco.
        - Erro inesperado durante múltiplas operações dentro da mesma transação.
    """
    pass
