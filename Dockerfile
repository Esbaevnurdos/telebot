FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Set environment variable for Python path
ENV PYTHONPATH="/app"

# Copy requirements.txt to install dependencies
COPY requirements.txt /app/

# Copy the bot Python file
COPY bot/todo_bot.py /app/bot/

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for PostgreSQL URI
ENV POSTGRES_URI=postgresql://postgres:password@postgres:5432/todo

# Run the bot script
CMD ["python", "/app/bot/todo_bot.py"]
