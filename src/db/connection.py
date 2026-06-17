"""
Módulo de conexão com SQLite.
"""

from pathlib import Path
import sqlite3

# caminho do banco
DB_PATH = Path(__file__).resolve().parent / "database" / "bot_at.db"


def get_connection() -> sqlite3.Connection:
    """Retorna conexão com o banco SQLite."""
    return sqlite3.connect(DB_PATH)