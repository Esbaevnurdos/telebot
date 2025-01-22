FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Set environment variable for Python path
ENV PYTHONPATH="/app"

# Copy requirements.txt to install dependencies
COPY requirements.txt /app/

# Copy the bot Python file
COPY bot/todo_bot.py /app/bot/

# Copy and prepare wait-for-it.sh script
COPY ./wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for MongoDB URI
ENV MONGO_URI=mongodb://mongo:27017/todo

# Run the bot script after ensuring MongoDB is ready
CMD ["/wait-for-it.sh", "mongo:27017", "--", "python", "/app/bot/todo_bot.py"]
