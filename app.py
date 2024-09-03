from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
import random
from telegram_bot import send_message
from scheduler import workout_messages, hydration_messages, break_messages

app = Flask(__name__)

# Specify the template folder location
app = Flask(__name__, template_folder='templates')

# Define the trigger for daily execution at 15:00
daily_trigger = CronTrigger(hour=15, minute=0)

# Initialize the scheduler
scheduler = BackgroundScheduler()

@app.route('/')
def home():
    try:
        # Avoid adding the job multiple times by checking if it already exists
        if not scheduler.get_job('daily_task'):
            scheduler.add_job(
                func=send_message,
                trigger=daily_trigger,
                id='daily_task',
                name='Run daily task at 15:00 every day',
                args=[random.choice(workout_messages)],
                replace_existing=True
            )
            print("Daily task scheduled.")

        # Schedule hydration reminders
        total_cups = 11.5
        total_minutes = 11 * 60
        interval_minutes = total_minutes / total_cups

        try:
            scheduler.add_job(
            func=lambda: send_message(random.choice(hydration_messages)),
            trigger=IntervalTrigger(minutes=interval_minutes),
            id='hydration_reminder',
            name='Hydration message',
            replace_existing=True
)       
        except Exception as e:
            print(f"Failed to add job: {e}")
            
        print(f"Hydration reminder scheduled.")

        if not scheduler.get_job('break_reminder'):
            scheduler.add_job(
                func=lambda: send_message(random.choice(break_messages)),
                trigger=IntervalTrigger(minutes=30),  # Set to remind every 30 minutes
                id='break_reminder',
                name='Remind to take a break every 30 minutes',
                replace_existing=True
            )
            print("Break reminder scheduled.")
            
        # Start the scheduler if it hasn't been started already
        if not scheduler.running:
            scheduler.start()
            print("Scheduler started.")
        else:
            print("Scheduler is already running.")
            
        return render_template('home.html')

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "error", "details": str(e)}, 500

@app.route('/stop', methods=['POST'])
def stop():
    try:
        # Attempt to shut down the scheduler
        scheduler.shutdown()
        return render_template('stopped.html')
    except Exception as e:
        # Handle other unexpected errors
        app.logger.error(f"Unexpected error while stopping the scheduler: {e}")
        return render_template('error.html', message="An unexpected error occurred.")

if __name__ == '__main__':
    app.run(debug=True, port=5002)
