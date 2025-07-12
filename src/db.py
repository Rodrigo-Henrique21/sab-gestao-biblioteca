import os
import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    return psycopg2.connect(os.environ["DATABASE_URL"])

@contextmanager
def get_cursor(commit=False):
    """
    Exemplo:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM livros")
    """
    conn = get_conn()
    cur = conn.cursor()
    try:
        yield cur
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
