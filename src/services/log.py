"""
Registro de consultas do bot.
"""

from src.db.bot_db import get_connection


def registrar_consulta(telegram_id: str, tipo: str, dado: str, instalacao: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO consultas (telegram_id, tipo, dado, instalacao)
            VALUES (?, ?, ?, ?)
        """, (
            telegram_id,
            tipo,
            dado,
            instalacao
        ))

        conn.commit()
