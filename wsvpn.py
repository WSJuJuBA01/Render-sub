from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from flask import Flask
import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context):
    await update.message.reply_text("Привет! Я простой бот. Напиши мне что-нибудь :)")

async def echo(update: Update, context):
    await update.message.reply_text(f"Ты написал: {update.message.text}")

def main():
    # Создаем приложение бота
    app_bot = Application.builder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("Бот запущен...")
    app_bot.run_polling()

if _name_ == "_main_":  # ← ВАЖНО! ДВА ПОДЧЕРКИВАНИЯ!
    main()
