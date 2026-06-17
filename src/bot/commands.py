"""
Comandos do bot.
"""

from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def teclado_menu(admin=False):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(
        KeyboardButton("🏠 Unidade Consumidora"),
        KeyboardButton("📟 Medidor"),
    )

    if admin:
        markup.add(
            KeyboardButton("👤 Cadastrar Usuário")
        )

    return markup
