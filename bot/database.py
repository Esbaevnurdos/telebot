import psycopg2
from psycopg2.extras import RealDictCursor
import os

# PostgreSQL connection
POSTGRES_URI = os.getenv("POSTGRES_URI", "postgresql://user:password@localhost:5432/todo")
conn = psycopg2.connect(POSTGRES_URI, cursor_factory=RealDictCursor)
cursor = conn.cursor()

# Ensure the tasks table exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        task TEXT NOT NULL,
        completed BOOLEAN DEFAULT FALSE
    );
""")
conn.commit()

# Add a task to PostgreSQL
def add_task(user_id, task):
    query = "INSERT INTO tasks (user_id, task) VALUES (%s, %s)"
    cursor.execute(query, (user_id, task))
    conn.commit()

# Get tasks from PostgreSQL for a specific user
def get_tasks(user_id):
    query = "SELECT * FROM tasks WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

# Mark a task as completed
def mark_task_completed(user_id, task_id):
    query = "UPDATE tasks SET completed = TRUE WHERE id = %s AND user_id = %s AND completed = FALSE"
    cursor.execute(query, (task_id, user_id))
    conn.commit()
    return cursor.rowcount > 0

# Edit a task
def edit_task(user_id, task_id, new_task):
    query = "UPDATE tasks SET task = %s WHERE id = %s AND user_id = %s"
    cursor.execute(query, (new_task, task_id, user_id))
    conn.commit()
    return cursor.rowcount > 0

# Remove a task
def remove_task(user_id, task_id):
    query = "DELETE FROM tasks WHERE id = %s AND user_id = %s"
    cursor.execute(query, (task_id, user_id))
    conn.commit()
    return cursor.rowcount > 0
