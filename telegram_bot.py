import requests
from config import Config
from datetime import datetime
import pytz
from scheduler import hydration_messages
import random

def send_message(message):
    url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': Config.TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)

def hydration_job():
    armenian_tz = pytz.timezone('Asia/Yerevan')
    current_time = datetime.now(armenian_tz).time()
    cutoff_time = datetime.strptime('21:00:00', '%H:%M:%S').time()
    
    if current_time < cutoff_time:
        # Call the universal send_message function
        send_message(random.choice(hydration_messages))