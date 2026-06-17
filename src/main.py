"""
Inicialização do bot.
"""

import time
import os
from telebot import TeleBot
from dotenv import load_dotenv
from telebot.types import BotCommand

from src.bot.handlers import register_handlers
from src.db.bot_db import init_db

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = TeleBot(TOKEN)

init_db()

bot.set_my_commands([
    BotCommand("menu", "Abrir menu"),
])



def run():
    print("🚀 Bot rodando...")

    register_handlers(bot)

    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(5)


if __name__ == "__main__":
    run()
