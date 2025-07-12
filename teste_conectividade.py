import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

conn = psycopg2.connect(os.environ["DATABASE_URL"])
with conn.cursor() as cur:
    cur.execute("SELECT * FROM public.livros LIMIT 5;")
    print(cur.fetchone())