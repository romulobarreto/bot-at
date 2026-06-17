from src.db.bot_db import get_connection


def delete_user(telegram_id: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM usuarios WHERE telegram_id = ?",
            (telegram_id,)
        )

        conn.commit()

    print(f"🗑️ Usuário removido: {telegram_id}")


if __name__ == "__main__":
    # 🔥 TROCA AQUI
    delete_user("634838365")