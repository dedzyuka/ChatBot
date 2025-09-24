import psycopg
from langgraph.checkpoint.postgres import PostgresSaver
from utils.config import POSTGRES_URL

def get_checkpointer():
    print("📡 Подключение к Postgres:", POSTGRES_URL)  # отладка
    conn = psycopg.connect(POSTGRES_URL, autocommit=True)
    saver = PostgresSaver(conn)
    saver.setup()  # создаст таблицы
    print("✅ setup() вызван, таблицы должны быть созданы")
    return saver
