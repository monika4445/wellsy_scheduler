from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
import random
from app.telegram_bot import send_message
from app.scheduler import workout_messages, hydration_messages

app = Flask(__name__)

# Define the trigger for daily execution at 20:56
daily_trigger = CronTrigger(hour=15, minute=0)

# Initialize the scheduler
scheduler = BackgroundScheduler()

@app.route('/')
def home():
    try:
        # Avoid adding the job multiple times by checking if it already exists
        if not scheduler.get_job('daily_task'):
            scheduler.add_job(
                func=lambda: send_message(random.choice(workout_messages)),
                trigger=daily_trigger,
                id='daily_task',
                name='Run daily task at 20:56 every day',
                replace_existing=True
            )
            print("Daily task scheduled.")

        # Schedule hydration reminders
        start_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        total_cups = 11.5
        total_minutes = 11 * 60
        interval_minutes = total_minutes / total_cups

        # Remove existing hydration reminder jobs
        for job in scheduler.get_jobs():
            if job.id.startswith('hydration_'):
                scheduler.remove_job(job.id)

        for i in range(int(total_cups)):
            reminder_time = start_time + timedelta(minutes=i * interval_minutes)
            scheduler.add_job(
                func=lambda: send_message(random.choice(hydration_messages)),
                trigger=IntervalTrigger(minutes=interval_minutes, start_date=reminder_time),
                id=f'hydration_{i}',
                name=f'Hydration reminder {i}'
            )
            print(f"Hydration reminder {i} scheduled.")

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
    app.run(debug=True)
