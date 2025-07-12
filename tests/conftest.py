# tests/conftest.py
import os, psycopg2, pytest
from dotenv import load_dotenv
load_dotenv(".env.test")

@pytest.fixture(autouse=True, scope="function")
def clear_db(monkeypatch):
    """
    Limpa tabelas e garante que todos os módulos usem o banco de testes.
    """
    test_url = os.environ["DATABASE_URL_TEST"]
    monkeypatch.setenv("DATABASE_URL", test_url)   # força src/db.py

    conn = psycopg2.connect(test_url)
    conn.autocommit = True        # para poder TRUNCATE fora de transação
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE vendas CASCADE;")
    cur.execute("TRUNCATE TABLE livros CASCADE;")
    cur.execute("TRUNCATE TABLE clientes CASCADE;")
    cur.close()
    conn.close()
    yield
    # nada a fazer depois – cada teste começa sempre limpo
