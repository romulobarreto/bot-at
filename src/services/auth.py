from src.db.bot_db import get_connection


def buscar_usuario(telegram_id: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT autorizado, administrador, prefixo
            FROM usuarios
            WHERE telegram_id = ?
        """, (telegram_id,))

        row = cursor.fetchone()

        if row:
            autorizado, administrador, prefixo = row
            return {
                "autorizado": autorizado,
                "administrador": administrador,
                "prefixo": prefixo
            }

        return None