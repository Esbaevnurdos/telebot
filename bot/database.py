from pymongo import MongoClient
import os
from bson import ObjectId

# MongoDB URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

# Select database and collection
db = client["todo"]
tasks_collection = db["tasks"]

# Test MongoDB connection
try:
    client.admin.command("ping")
    print("Connected to MongoDB!")
except Exception as e:
    print("Error connecting to MongoDB:", e)

# Add a task to MongoDB
def add_task(user_id, task):
    task_document = {
        "user_id": user_id,
        "task": task,
        "completed": False,
    }
    tasks_collection.insert_one(task_document)

# Get tasks from MongoDB for a specific user
def get_tasks(user_id):
    return list(tasks_collection.find({"user_id": user_id}))

# Mark task as completed
def mark_task_completed(user_id, task_id):
    result = tasks_collection.update_one(
        {"_id": ObjectId(task_id), "user_id": user_id, "completed": False},
        {"$set": {"completed": True}}
    )
    return result.matched_count > 0

# Edit a task
def edit_task(user_id, task_id, new_task):
    result = tasks_collection.update_one(
        {"_id": ObjectId(task_id), "user_id": user_id},
        {"$set": {"task": new_task}}
    )
    return result.matched_count > 0

# Remove a task
def remove_task(user_id, task_id):
    result = tasks_collection.delete_one(
        {"_id": ObjectId(task_id), "user_id": user_id}
    )
    return result.deleted_count > 0
