import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")     
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not TOKEN or not ADMIN_ID:
    logger.error("Не заданы переменные окружения TOKEN и/или ADMIN_ID")
    raise SystemExit("Задайте TOKEN и ADMIN_ID как env vars")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! 👋 Отправь сюда своё домашнее задание, и я передам его куратору.")

async def forward_homework(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.forward(chat_id=ADMIN_ID)
        await update.message.reply_text("✅ Домашнее задание принято! Ждите проверки.")
    except Exception as e:
        logger.error(f"Ошибка пересылки: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, forward_homework))
    logger.info("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
