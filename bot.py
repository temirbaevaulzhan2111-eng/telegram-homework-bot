import os
import telebot
from flask import Flask
import threading


TOKEN = os.environ.get("TELEGRAM_TOKEN")
MY_ID = int(os.environ.get("MY_ID"))

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет 👋! Отправь сюда своё домашнее задание (текст или фото)." 
                 
@bot.message_handler(content_types=['text'])
def forward_text(message):
    bot.send_message(MY_ID, f"📩 Новое сообщение от {message.from_user.first_name}:\n\n{message.text}")


@bot.message_handler(content_types=['photo'])
def forward_photo(message):
    photo_id = message.photo[-1].file_id
    caption = message.caption if message.caption else "📷 Фото без подписи"
    bot.send_photo(MY_ID, photo_id, caption=f"От {message.from_user.first_name}:\n{caption}")


app = Flask('')

@app.route('/')
def home():
    return "✅ Бот работает и не спит!"

def run():
    app.run(host='0.0.0.0', port=8080)


if name == "__main__":
    threading.Thread(target=run).start()
    print("✅ Бот запущен и слушает сообщения...")
    bot.infinity_polling()

