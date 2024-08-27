# Life Updates Scheduler

This project is a Flask application that uses a scheduler to send hydration reminders, and workout notifications to you via Telegram.

## Features

- Sends friendly workout reminders to encourage you to stay active.
- Sends hydration reminders to help you maintain proper hydration throughout the day.
- Customizable scheduling options for both workouts and hydration reminders.

## Setup Instructions

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/wellsyscheduler.git
    cd wellsyscheduler
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file based on the `.env.example`:

    ```bash
    cp .env.example .env
    ```

    Fill in your environment variables in the `.env` file, including your Telegram bot token and chat ID.

4. Run the Flask application:

    ```bash
    python app.py
    ```

5. Start the scheduler by making a POST request to the `/start-scheduler` endpoint to begin receiving updates:

    ```bash
    curl -X POST http://localhost:5000/start-scheduler
    ```

6. Your scheduler will now be running, sending hydration and workout reminders to you via Telegram!

## Usage

- The bot will send hydration reminders multiple times a day to ensure you stay hydrated.
- Workout reminders will be sent daily to motivate you to keep moving.

## Environment Variables

- `SECRET_KEY`: A secret key for your Flask application.
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
- `TELEGRAM_CHAT_ID`: Your chat ID to send messages.

## License

This project is licensed under the MIT License.
