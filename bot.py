import os
import telebot
from flask import Flask, request
import logging

# ==================== НАСТРОЙКИ ====================
TOKEN = os.environ.get("TELEGRAM_TOKEN")  # токен бота из @BotFather
MY_ID = 1464067257  # твой Telegram ID
RENDER_URL = os.environ.get("RENDER_URL")  # URL проекта на Render, например https://имя.onrender.com

# Проверяем, что все переменные есть
if not TOKEN or not RENDER_URL:
    raise SystemExit("❌ Ошибка: не заданы TELEGRAM_TOKEN или RENDER_URL в Render Environment Variables")

# ==================== ЛОГИ ====================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ==================== БОТ + FLASK ====================
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    logger.info("Получена команда /start")
    bot.send_message(message.chat.id, "Привет! Отправь сюда своё домашнее задание 📚")

# Обработка фотографий
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    logger.info("Получено фото")
    caption = message.caption if message.caption else "(без подписи)"
    file_id = message.photo[-1].file_id

    # Отправляем фото куратору
    try:
        bot.send_photo(MY_ID, file_id, caption=f"📸 От {message.from_user.first_name}:\n{caption}")
    except Exception as e:
        logger.error(f"Ошибка при пересылке фото: {e}")

    # Ответ ученику
    bot.send_message(message.chat.id, "✅ Домашнее задание отправлено преподавателю!")

# Обработка текста
@bot.message_handler(content_types=['text'])
def handle_text(message):
    logger.info("Получено текстовое сообщение")

    # Отправляем текст куратору
    try:
        bot.send_message(MY_ID, f"✉️ Сообщение от {message.from_user.first_name}: {message.text}")
    except Exception as e:
        logger.error(f"Ошибка при пересылке текста: {e}")

    # Ответ ученику
    bot.send_message(message.chat.id, "✅ Сообщение отправлено преподавателю!")

# Вебхук
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_str = request.data.decode("utf-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return "", 200
    return "OK", 200

# Главная страница
@app.route('/')
def index():
    return "✅ Бот работает!"

# Устанавливаем вебхук
try:
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + '/' + TOKEN)
    logger.info("Вебхук успешно установлен")
except Exception as e:
    logger.error(f"Ошибка при установке вебхука: {e}")

# Запуск (локально)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))



