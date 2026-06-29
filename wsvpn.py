from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from flask import Flask
from threading import Thread
import os
import time
import requests

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context):
    await update.message.reply_text("Привет! Я простой бот. Напиши мне что-нибудь :)")

async def echo(update: Update, context):
    await update.message.reply_text(f"Ты написал: {update.message.text}")

app_bot = Application.builder().token(TOKEN).build()
app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

flask_app = Flask("wsvpn")

@flask_app.route('/')
def home():
    return "Бот работает!"

@flask_app.route('/ping')
def ping():
    return "OK", 200

@flask_app.route('/health')
def health():
    return "OK", 200

def run_bot():
    print("Бот запущен...")
    while True:
        try:
            app_bot.run_polling()
        except Exception as e:
            print(f"Ошибка бота: {e}")
            time.sleep(5)

def keep_alive():
    """Пинг сам себя чтобы не уснул на Render"""
    url = os.getenv('RENDER_EXTERNAL_URL', '')
    if not url:
        url = os.getenv('PUBLIC_URL', '')
    if not url:
        url = 'https://wsvpn-bobot.onrender.com'  # ← ВАШ URL!
    url = url.rstrip('/')
    
    print(f"[keep_alive] Запущен пинг для {url}")
    while True:
        try:
            requests.get(f"{url}/ping", timeout=10)
            print(f"[keep_alive] Пинг в {time.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"[keep_alive] Ошибка: {e}")
        time.sleep(240)

# Запускаем бота в фоновом потоке
Thread(target=run_bot, daemon=True).start()

# Запускаем пинг (чтобы не уснул)
Thread(target=keep_alive, daemon=True).start()

# Запускаем Flask
if name == "main":
    port = int(os.getenv("PORT", 10000))
    print(f"🚀 Сервер запущен на порту {port}")
    flask_app.run(host="0.0.0.0", port=port)
