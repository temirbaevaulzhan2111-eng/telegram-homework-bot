import os
from flask import Flask, request
import requests

TOKEN = os.environ.get("TELEGRAM_TOKEN")  # токен из Render (Environment)
ADMIN_ID = 1464067257  # твой Telegram ID

app = Flask(__name__)
URL = f"https://api.telegram.org/bot{TOKEN}"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]

        # --- обработка команды /start ---
        if "text" in message and message["text"] == "/start":
            send_message(chat_id, "Привет! Мы приняли твое домашнее задание")

        # --- если ученик прислал фото ---
        elif "photo" in message:
            file_id = message["photo"][-1]["file_id"]  # лучшее качество фото
            caption = message.get("caption", "")       # текст под фото (если есть)

            # имя/username ученика
            user = message["from"]
            student_name = user.get("username") or user.get("first_name") or "Ученик"

            final_caption = f"Домашка от {student_name}:\n{caption}"

            forward_photo_with_caption(ADMIN_ID, file_id, final_caption)

    return "ok", 200

# отправка текста
def send_message(chat_id, text):
    url = f"{URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# пересылка фото с подписью
def forward_photo_with_caption(chat_id, file_id, caption=""):
    url = f"{URL}/sendPhoto"
    payload = {
        "chat_id": chat_id,
        "photo": file_id,
        "caption": caption
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)




