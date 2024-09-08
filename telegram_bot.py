import requests
from config import Config
from datetime import datetime
import pytz

def send_message(message):
    armenian_tz = pytz.timezone('Asia/Yerevan')
    current_time = datetime.now(armenian_tz).time()
    cutoff_time = datetime.strptime('21:00:00', '%H:%M:%S').time()
    
    if current_time < cutoff_time:
        url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': Config.TELEGRAM_CHAT_ID,
            'text': message
        }
        requests.post(url, data=payload)
