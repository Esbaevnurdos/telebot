from celery import Celery
from datetime import datetime
from bot.database import get_pending_tasks, send_reminder_message

# Initialize the Celery app

app = Celery('tasks', broker='redis://redis:6379/0')

# Define a periodic task for sending reminders
@app.task
def send_task_reminder():
    tasks = get_pending_tasks()
    for task in tasks:
        # You could add a check for task due date, if applicable
        message = f"Reminder: You have a pending task: {task['title']}"
        send_reminder_message(task['user_id'], message)
        print(f"Reminder sent for task: {task['title']}")

