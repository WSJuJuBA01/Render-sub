from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from flask import Flask
from threading import Thread
import os

TOKEN = os.getenv("TOKEN")  # Токен из переменных окружения Render

# ---------- БОТ ----------
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я простой бот. Напиши мне что-нибудь :)")

async def echo(update: Update, context):
    await update.message.reply_text(f"Ты написал: {update.message.text}")

app_bot = Application.builder().token(TOKEN).build()
app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# ---------- ВЕБ-СЕРВЕР ДЛЯ RENDER ----------
flask_app = Flask(name)

@flask_app.route('/')
def home():
    return "Бот работает!"

def run_bot():
    print("Бот запущен...")
    app_bot.run_polling()

# Запускаем бота в фоновом потоке
Thread(target=run_bot).start()

# Запускаем Flask (это увидит Render)
if name == "main":
    flask_app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
