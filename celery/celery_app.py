from celery import Celery
import os
from bot.database import get_tasks

REDIS_URL = os.getenv("REDIS_URL")
celery_app = Celery("tasks", broker=REDIS_URL)

@celery_app.task
def send_reminders():
    # Logic to send reminders to users about pending tasks
    tasks = get_pending_tasks()

    # Loop through the tasks and send reminders to users
    for task in tasks:
        user_id = task['user_id']  # Assuming user_id is part of the task
        task_title = task['title']  # Assuming title is part of the task
        
        # Craft the reminder message
        reminder_message = f"Reminder: You have a pending task: {task_title}"

        # Send the reminder message via Telegram bot
        bot.send_message(user_id, reminder_message)
        print(f"Reminder sent to {user_id} for task: {task_title}")
    pass
