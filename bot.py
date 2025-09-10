from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = "8246209633:AAFQtQZbnRzDGDyWo5QGXFU1JYxn-C9ILek"
CHAT_ID = 1464067257  # твой айди

URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # Ответ пользователю
        requests.post(URL, json={"chat_id": chat_id, "text": f"Ты написал: {text}"})

        # Уведомление только тебе
        requests.post(URL, json={"chat_id": CHAT_ID, "text": f"Пользователь {chat_id} написал: {text}"})

    return {"ok": True}


@app.route("/", methods=["GET"])
def home():
    return "Бот работает!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


