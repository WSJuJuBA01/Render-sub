from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = "8832833214:AAH7l7_F6ruYd6D0tUDXqqsMbJlrM3Ll_E0"  # Получить у @BotFather

async def start(update: Update, context):
    await update.message.reply_text("Привет! Я простой бот. Напиши мне что-нибудь :)")

async def echo(update: Update, context):
    await update.message.reply_text(f"Ты написал: {update.message.text}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

print("Бот запущен...")
app.run_polling()
