import sqlite3
from pathlib import Path

# caminho do banco
DB_PATH = Path(__file__).resolve().parent / "database" / "bot.db"


def get_connection():
    """Retorna conexão com o banco do bot."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """Inicializa banco e cria tabelas se não existirem."""

    # garante pasta
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # =========================
        # 👤 USUÁRIOS
        # =========================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id TEXT UNIQUE,
                prefixo TEXT,
                autorizado INTEGER DEFAULT 0,
                administrador INTEGER DEFAULT 0
            )
        """)


        # =========================
        # 📊 CONSULTAS
        # =========================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tipo TEXT,
                dado TEXT,
                instalacao TEXT,
                telegram_id TEXT
            )
        """)


        conn.commit()
