import psycopg
from langgraph.checkpoint.postgres import PostgresSaver
from utils.config import POSTGRES_URL

def get_checkpointer():
    print("📡 Подключение к Postgres:", POSTGRES_URL)
    conn = psycopg.connect(POSTGRES_URL, autocommit=True)
    saver = PostgresSaver(conn)
    saver.setup()
    print("✅ Extensions:", conn.execute("SELECT * FROM pg_extension;").fetchall())
    return saver
