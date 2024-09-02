import requests
from config import Config

def send_message(message):
    url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': Config.TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)