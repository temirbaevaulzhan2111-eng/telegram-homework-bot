
import os
import telebot
from flask import Flask, request
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


TOKEN = os.environ.get("TELEGRAM_TOKEN")
MY_ID = int(os.environ.get("MY_ID"))
RENDER_URL = os.environ.get("RENDER_URL")


bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    logger.info("Получена команда /start.")
    bot.send_message(message.chat.id, "Привет! Отправь сюда своё домашнее задание 📚")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    logger.info("Получено фото.")
    caption = message.caption if message.caption else "(без подписи)"
    file_id = message.photo[-1].file_id
    
    
    bot.send_photo(MY_ID, file_id, caption=f"От {message.from_user.first_name}:\n{caption}")
    bot.send_message(message.chat.id, "✅ Домашнее задание отправлено преподавателю!")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    logger.info("Получено текстовое сообщение.")
   
    bot.send_message(MY_ID, f"✉️ Сообщение от {message.from_user.first_name}: {message.text}")
    bot.send_message(message.chat.id, "✅ Сообщение отправлено преподавателю!")

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.data.decode("utf-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '', 200
    return "OK", 200


@app.route('/')
def index():
    return "✅ Бот работает!"

if RENDER_URL:
    try:
       
        bot.remove_webhook()
      
        bot.set_webhook(url=RENDER_URL + '/' + TOKEN)
        logger.info("Вебхук успешно установлен.")
    except Exception as e:
        logger.error(f"Ошибка при установке вебхука: {e}")
else:
    logger.info("Переменная RENDER_URL не найдена. Вебхук не будет установлен.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))



