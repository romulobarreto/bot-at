"""
Handlers do bot.
"""

from telebot.types import Message
from telebot import TeleBot

from src.bot.commands import teclado_menu

from src.services.cadastro import (
    buscar_por_instalacao,
    buscar_por_medidor,
)

from src.services.equipamentos import buscar_equipamentos
from src.services.consumo import buscar_consumo
from src.services.coordenadas import buscar_coordenadas
from src.services.log import registrar_consulta
from src.services.auth import buscar_usuario

from src.db.bot_db import get_connection

from src.utils.formatter import (
    formatar_cadastro,
    formatar_equipamento,
)

from src.utils.image import gerar_imagem_tabela

# 🔥 controle de estado
contexto_usuario = {}


def get_menu_usuario(telegram_id: str):
    usuario = buscar_usuario(telegram_id)

    if usuario and usuario["autorizado"] == 1:
        return teclado_menu(admin=usuario["administrador"] == 1)

    return teclado_menu()



def register_handlers(bot: TeleBot):

    # =========================
    # ✅ START
    # =========================
    @bot.message_handler(commands=["start", "menu"])
    def start(message: Message):

        contexto_usuario.pop(message.chat.id, None)

        telegram_id = str(message.from_user.id)
        usuario = buscar_usuario(telegram_id)

        # ❌ NÃO EXISTE
        if usuario is None:
            bot.send_message(
                message.chat.id,
                f"""👋 Bem Vindo, sou o Bot de Atendimento da EQTL RS Grupo A!

Para acesso ao Bot, envie ao administrador:

🧑🏼‍💻 Rômulo Barreto da Silva  
📞 (53) 997048858  

- Sua equipe (Prefixo)  
- ID usuário  

🆔 Seu ID:
{telegram_id}
"""
            )
            return

        # ❌ NÃO AUTORIZADO
        if usuario["autorizado"] == 0:
            bot.send_message(
                message.chat.id,
                f"""⏳ Aguardando liberação...

🆔 Seu ID:
{telegram_id}
"""
            )
            return

        # ✅ AUTORIZADO
        bot.send_message(
            message.chat.id,
            f"✅ Bem vindo! ({usuario['prefixo']})",
            reply_markup=get_menu_usuario(str(message.from_user.id))
        )

    # =========================
    # ✅ MENU PRINCIPAL
    # =========================
    @bot.message_handler(func=lambda m: m.text in [
        "🏠 Unidade Consumidora",
        "📟 Medidor"
    ])
    def escolher_tipo(message: Message):

        contexto_usuario[message.chat.id] = m = (
            "INSTALACAO" if message.text == "🏠 Unidade Consumidora" else "MEDIDOR"
        )

        bot.send_message(
            message.chat.id,
            "🔢 Informe o número:"
        )

    # =========================
    # 👤 CADASTRAR USUÁRIO (ADMIN)
    # =========================
    @bot.message_handler(func=lambda m: m.text == "👤 Cadastrar Usuário")
    def cadastrar_usuario_inicio(message: Message):

        telegram_id = str(message.from_user.id)
        usuario = buscar_usuario(telegram_id)

        if not usuario or usuario["administrador"] == 0:
            bot.send_message(message.chat.id, "❌ Sem permissão.")
            return

        contexto_usuario[message.chat.id] = "CADASTRO"

        bot.send_message(
            message.chat.id,
            "📥 Envie no formato:\n\nID PREFIXO\n\nExemplo:\n123456 RS-PEL-A001"
        )

    @bot.message_handler(func=lambda m: contexto_usuario.get(m.chat.id) == "CADASTRO")
    def cadastrar_usuario(message: Message):

        try:
            partes = message.text.split()

            if len(partes) != 2:
                bot.send_message(message.chat.id, "❌ Formato inválido.")
                return

            novo_id, prefixo = partes

            with get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT OR IGNORE INTO usuarios (telegram_id, prefixo, autorizado)
                    VALUES (?, ?, 1)
                """, (novo_id, prefixo))

                conn.commit()

            bot.send_message(
                message.chat.id,
                f"✅ Usuário {novo_id} cadastrado!"
            )

        except Exception as e:
            print(e)
            bot.send_message(message.chat.id, "❌ Erro ao cadastrar.")

        finally:
            contexto_usuario.pop(message.chat.id, None)

    # =========================
    # 🔍 PROCESSAR CONSULTA
    # =========================
    @bot.message_handler(func=lambda m: m.text.isdigit())
    def processar_numero(message: Message):

        telegram_id = str(message.from_user.id)
        usuario = buscar_usuario(telegram_id)

        if usuario is None or usuario["autorizado"] == 0:
            bot.send_message(message.chat.id, "❌ Sem permissão.")
            return

        try:
            contexto = contexto_usuario.get(message.chat.id)

            if not contexto:
                bot.send_message(message.chat.id, "❗ Use o menu.")
                return

            numero = message.text

            # 🔍 BUSCA
            if contexto == "INSTALACAO":
                resultado = buscar_por_instalacao(numero)
            else:
                resultado = buscar_por_medidor(numero)

            if resultado is None:
                bot.send_message(message.chat.id, "⚠️ Não encontrado.")
                return

            instalacao = str(resultado["INSTALACAO"]).strip()

            # ✅ LOG
            registrar_consulta(
                telegram_id=telegram_id,
                tipo=contexto,
                dado=numero,
                instalacao=instalacao
            )

            # 📄 CADASTRO
            bot.send_message(message.chat.id, formatar_cadastro(resultado))

            # ⚙️ EQUIPAMENTOS
            equipamentos = buscar_equipamentos(instalacao)
            equipamentos = sorted(
                equipamentos,
                key=lambda x: (x.get("EQUIPAMENTO", ""), str(x.get("NUM_EQUIPAMENTO", "")))
            )

            if equipamentos:
                bot.send_message(message.chat.id, f"🔌 {len(equipamentos)} equipamentos")

                for eq in equipamentos:
                    bot.send_message(message.chat.id, formatar_equipamento(eq))

            # 📊 CONSUMO
            df = buscar_consumo(instalacao)
            if df is not None:
                img = gerar_imagem_tabela(df)
                bot.send_photo(message.chat.id, img, caption="📊 Consumo")

            # 📍 MAPA
            lat, lon = buscar_coordenadas(instalacao)

            if lat and lon:
                bot.send_message(
                    message.chat.id,
                    f"📍 https://www.google.com/maps?q={lat},{lon}"
                )

            # ✅ FINAL
            bot.send_message(
                message.chat.id,
                "✅ Consulta finalizada.",
                reply_markup=get_menu_usuario(str(message.from_user.id))
            )

            contexto_usuario.pop(message.chat.id, None)

        except Exception as e:
            print(e)
            bot.send_message(message.chat.id, "❌ Erro.")

    # =========================
    # ✅ FALLBACK
    # =========================
    @bot.message_handler(func=lambda m: True)
    def fallback(message: Message):
        bot.send_message(message.chat.id, "❗ Use o menu.", reply_markup=get_menu_usuario(str(message.from_user.id)))
