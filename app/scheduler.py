from .telegram_bot import send_message
import random
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

def schedule_workout_and_hydration_reminders():
    workout_messages = [
        "Hey there, future fitness queen! Your workout wants your attention!",
        "Remember: A good coder takes breaks! Time for your workout!",
        "Rise up, supergirl! Your workout is waiting! You are unstoppable!",
        "Today’s workout is a chance to prove how strong you truly are. Let’s get to it!",
        "It’s workout time! Each session is an opportunity to improve yourself and build resilience. Let’s do this!",
        "Time to get moving! Remember, every workout is a step toward your best self. Enjoy the process, and let’s achieve those fitness goals together!",
        "Workout time! Every moment you dedicate to your fitness is an investment in your well-being. Stay committed. You’re amazing!"
    ]

    hydration_messages = [
        "Don’t forget to hydrate! Your body will thank you later.",
        "Water time! Keep that brain and body fueled.",
        "Time to sip some water—stay refreshed and ready to take on the world!",
        "Your hydration break is here! Grab a glass of water and keep going strong.",
        "Hydrate, hydrate, hydrate! It’s the fuel your body needs.",
        "Pause and refresh! A quick water break keeps you at your best.",
        "You’ve got this! But first, a sip of water to keep you going."
    ]

    # Initialize the scheduler
    scheduler = BackgroundScheduler()

    # Schedule workout reminders (e.g., once a day)
    scheduler.add_job(func=lambda: send_message(random.choice(workout_messages)), trigger=CronTrigger(hour=13, minute=27))

    # Schedule hydration reminders (e.g., 8 times a day)
    hydration_times = 8  # Number of times to remind to drink water
    hydration_interval = 24 // hydration_times  # Calculate the interval in hours

    scheduler.add_job(func=lambda: send_message(random.choice(hydration_messages)), trigger=IntervalTrigger(hours=hydration_interval, start_date=f'2024-08-27 07:00:00'))

    scheduler.start()