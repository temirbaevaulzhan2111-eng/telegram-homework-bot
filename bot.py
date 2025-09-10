import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get("TELEGRAM_TOKEN")
MY_ID = int(os.environ.get("MY_ID"))

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)  


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Отправь сюда своё домашнее задание 📚")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    caption = message.caption if message.caption else "(без подписи)"
    file_id = message.photo[-1].file_id

 
    bot.send_photo(MY_ID, file_id, caption=caption)
    bot.send_message(message.chat.id, "✅ Домашнее задание отправлено преподавателю!")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(MY_ID, f"✉️ Сообщение от {message.from_user.first_name}: {message.text}")
    bot.send_message(message.chat.id, "✅ Сообщение отправлено преподавателю!")

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def index():
    return "✅ Бот работает!"

if name == "__main__":
   
    bot.infinity_polling()

