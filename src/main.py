# src/main.py
from datetime import date
from livros import cadastrar_livro, listar_livros, buscar, atualizar_estoque
from clientes import cadastrar_cliente, listar_clientes, obter_cliente_por_nome
from vendas import registrar_venda, listar_vendas, relatorio_diario
from errors import *

MENU = """
1 – Cadastrar livro
2 – Listar livros
3 – Buscar livro
4 – Cadastrar cliente
5 – Listar clientes
6 – Registrar venda
7 – Relatório de vendas (hoje)
0 – Sair
"""

def main():
    while True:
        print(MENU)
        op = input("Escolha: ").strip()
        try:
            if op == "1":
                titulo = input("Título: ")
                autor = input("Autor: ")
                isbn = input("ISBN: ")
                preco = float(input("Preço: "))
                estoque = int(input("Estoque: "))
                cadastrar_livro(titulo, autor, isbn, preco, estoque)
                print("Livro cadastrado!")
            elif op == "2":
                for l in listar_livros():
                    print(l)
            elif op == "3":
                termo = input("Digite parte do título/autor ou ISBN: ")
                encontrados = buscar(titulo=termo) + buscar(autor=termo) + buscar(isbn=termo)
                for l in {e[3]: e for e in encontrados}.values():
                    print(l)
            elif op == "4":
                nome = input("Nome: ")
                tel = input("Telefone: ")
                cadastrar_cliente(nome, tel)
                print("Cliente cadastrado!")
            elif op == "5":
                for c in listar_clientes():
                    print(c)
            elif op == "6":
                nome = input("Nome cliente: ")
                isbn = input("ISBN livro: ")
                qtd = int(input("Qtd: "))
                registrar_venda(nome, isbn, qtd)
                print("Venda registrada!")
            elif op == "7":
                total = relatorio_diario(date.today())
                print(f"Total vendido hoje: R$ {total}")
            elif op == "0":
                break
        except (LivroJaExisteError, ClienteJaExisteError, LivroNaoEncontradoError,
                ClienteNaoEncontradoError, EstoqueInsuficienteError, TransacaoErro) as e:
            print("Erro:", e)

if __name__ == "__main__":
    main()
