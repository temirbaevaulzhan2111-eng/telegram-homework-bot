# Импортируем необходимые библиотеки
import os
import telebot
from flask import Flask, request
import logging

# Настройка логирования для отладки
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Получаем переменные окружения, которые вы задали на Render
TOKEN = os.environ.get("TELEGRAM_TOKEN")
MY_ID = os.environ.get("MY_ID")
RENDER_URL = os.environ.get("RENDER_URL")

# Проверяем, что все переменные заданы, иначе завершаем работу
if not TOKEN or not MY_ID or not RENDER_URL:
    logger.error("ОШИБКА: Не заданы все необходимые переменные окружения. Проверьте TELEGRAM_TOKEN, MY_ID и RENDER_URL.")
    raise SystemExit("Программа остановлена.")

try:
    # Преобразуем MY_ID в число
    MY_ID = int(MY_ID)
except (ValueError, TypeError):
    logger.error("ОШИБКА: Переменная MY_ID должна быть числом.")
    raise SystemExit("Программа остановлена.")

# Создаем экземпляр бота и Flask-приложения
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    logger.info("Получена команда /start.")
    bot.send_message(message.chat.id, "Привет! Отправь сюда своё домашнее задание 📚")

# Обработчик фотографий
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    logger.info("Получено фото.")
    caption = message.caption if message.caption else "(без подписи)"
    file_id = message.photo[-1].file_id
    
    # Отправляем фото и его подпись куратору
    bot.send_photo(MY_ID, file_id, caption=f"От {message.from_user.first_name}:\n{caption}")
    bot.send_message(message.chat.id, "✅ Домашнее задание отправлено преподавателю!")

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    logger.info("Получено текстовое сообщение.")
    # Отправляем текст куратору
    bot.send_message(MY_ID, f"✉️ Сообщение от {message.from_user.first_name}: {message.text}")
    bot.send_message(message.chat.id, "✅ Сообщение отправлено преподавателю!")

# Маршрут для вебхука, который принимает сообщения от Telegram
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.data.decode("utf-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '', 200
    return "OK", 200

# Главная страница, чтобы проверить, что сервер работает
@app.route('/')
def index():
    return "✅ Бот работает!"

# Устанавливаем вебхук при каждом запуске приложения
if RENDER_URL:
    try:
        # Сначала удалим старый вебхук
        bot.remove_webhook()
        # Затем установим новый
        bot.set_webhook(url=RENDER_URL + '/' + TOKEN)
        logger.info("Вебхук успешно установлен.")
    except Exception as e:
        logger.error(f"Ошибка при установке вебхука: {e}")
else:
    logger.info("Переменная RENDER_URL не найдена. Вебхук не будет установлен.")

# Этот блок кода будет выполнен только при локальном запуске
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

