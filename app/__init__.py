from flask import Flask, render_template
from .config import Config  
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from .scheduler import schedule_workout_and_hydration_reminders

# Global variable to track scheduler state
scheduler_running = False
scheduler = None

def create_app():
    global scheduler
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the scheduler
    scheduler = BackgroundScheduler()

    # Route for the HTML page
    @app.route('/')
    def index():
        return render_template('home.html')
             
    @app.route('/start-scheduler', methods=['POST'])
    def start_scheduler():
        global scheduler_running
        if not scheduler_running:
            # Schedule the workout and hydration reminders
            schedule_workout_and_hydration_reminders()
            scheduler.start()
            scheduler_running = True
            return render_template('home.html')
        return render_template('home.html')

    @app.route('/stop-scheduler', methods=['POST']) 
    def stop_scheduler():
        global scheduler_running
        if scheduler_running:
            scheduler.shutdown(wait=False)
            scheduler_running = False
            return render_template('stopped.html') 
        return render_template('stopped.html') 

    return app
