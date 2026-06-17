from src.db.bot_db import get_connection

def create_user(telegram_id: str, prefixo: str, admin: int = 0):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO usuarios (
                telegram_id,
                prefixo,
                autorizado,
                administrador
            )
            VALUES (?, ?, ?, ?)
        """, (
            telegram_id,
            prefixo,
            1,      # já autorizado
            admin   # admin ou não
        ))

        conn.commit()

    print(f"✅ Usuário criado: {telegram_id}")


if __name__ == "__main__":
    # 🔥 ALTERA AQUI
    create_user(
        telegram_id="634838365",   # ID
        prefixo="ROMULO ADMIN",    # Prefixo ou pessoa
        admin=1                    # Administrador ou não
    )
