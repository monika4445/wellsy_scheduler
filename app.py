from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import logging
from telegram_bot import send_message
from scheduler import workout_messages, break_messages
import pytz
import random
from telegram_bot import hydration_job
from logging import Formatter
from datetime import datetime

# Define a custom formatter to use Armenian time
class ArmenianTimeFormatter(Formatter):
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
        self.timezone = pytz.timezone('Asia/Yerevan')

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, self.timezone)
        if datefmt:
            return dt.strftime(datefmt)
        else:
            return dt.isoformat()

# Set up logging configuration
formatter = ArmenianTimeFormatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Apply custom formatter to Flask and Werkzeug loggers
logging.basicConfig(level=logging.DEBUG, handlers=[console_handler])
logger = logging.getLogger(__name__)

# Specify the template folder location
app = Flask(__name__, template_folder='templates')

# Define the trigger for daily execution at 15:00 in Armenian time
armenian_tz = pytz.timezone('Asia/Yerevan')
daily_trigger = CronTrigger(hour=20, minute=7, timezone=armenian_tz)

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

@app.route('/')
def home():
    try:
        # Avoid adding the job multiple times by checking if it already exists
        scheduler.add_job(
            func=send_message,
            trigger=daily_trigger,
            id='daily_task',
            name='Run daily task at 15:00 every day',
            args=[random.choice(workout_messages)],
            replace_existing=True
        )
        logger.info("Daily task scheduled.")

        try:
            hydration_interval = IntervalTrigger(minutes=3) 
            scheduler.add_job(
                func=hydration_job,
                trigger=hydration_interval,
                id='hydration_reminder',
                name='Hydration message',
                replace_existing=True
            )       
            logger.info("Hydration reminder scheduled with an interval of 57 minutes.")
        except Exception as e:
                logger.error("Failed to add hydration reminder job: %s", e)

        scheduler.add_job(
            func=send_message,
            trigger=IntervalTrigger(minutes=3),
            id='break_reminder',
            name='Remind to take a break every 30 minutes',
            args=[random.choice(break_messages)],
            replace_existing=True
        )
        logger.info("Break reminder scheduled every 30 minutes.")

    except Exception as e:
        logger.error("An error occurred: %s", e)
        return {"message": "error", "details": str(e)}, 500

    return render_template('home.html')

@app.route('/stop', methods=['POST'])
def stop():
    try:
        if scheduler.running:
            scheduler.shutdown()
            logger.info("Scheduler stopped.")
        return render_template('stopped.html')
    except Exception as e:
        logger.error("Unexpected error while stopping the scheduler: %s", e)
        return render_template('error.html', message="An unexpected error occurred.")

if __name__ == '__main__':
    app.run(debug=True, port=5002)
