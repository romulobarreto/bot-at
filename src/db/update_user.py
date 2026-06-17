from src.db.bot_db import get_connection


def update_user(
    telegram_id: str,
    prefixo: str = None,
    autorizado: int = None,
    administrador: int = None
):
    with get_connection() as conn:
        cursor = conn.cursor()

        # monta dinamicamente
        campos = []
        valores = []

        if prefixo is not None:
            campos.append("prefixo = ?")
            valores.append(prefixo)

        if autorizado is not None:
            campos.append("autorizado = ?")
            valores.append(autorizado)

        if administrador is not None:
            campos.append("administrador = ?")
            valores.append(administrador)

        if not campos:
            print("⚠️ Nada para atualizar.")
            return

        valores.append(telegram_id)

        query = f"""
            UPDATE usuarios
            SET {", ".join(campos)}
            WHERE telegram_id = ?
        """

        cursor.execute(query, valores)
        conn.commit()

    print(f"✅ Usuário atualizado: {telegram_id}")


if __name__ == "__main__":
    # 🔥 EXEMPLOS (usa um por vez)

    # ✅ bloquear usuário
    update_user("634838365", autorizado=0)

    # ✅ liberar usuário
    # update_user("634838365", autorizado=1)

    # ✅ mudar prefixo
    # update_user("634838365", prefixo="RS-PEL-A002")

    # ✅ virar admin
    # update_user("634838365", administrador=1)