from aiogram import Dispatcher, types
from bot.database import add_task, get_tasks, mark_task_completed, edit_task, remove_task
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Command: /start
async def cmd_start(message: types.Message):
    await message.answer(
        "Welcome to the ToDo Bot! 🤖\n\n"
        "Available commands:\n"
        "✅ /add_task <task> - Add a new task\n"
        "📋 /list_tasks - List all your tasks\n"
        "✔️ /complete_task <task_id> - Mark a task as completed\n"
        "✏️ /edit_task <task_id> <new_task> - Edit an existing task\n"
        "❌ /remove_task <task_id> - Remove a task"
    )

# Command: /add_task
async def cmd_add_task(message: types.Message):
    task = message.get_args()
    if not task:
        await message.reply("Please provide a task description! 📝")
        return
    if len(task) > 255:
        await message.reply("Task description is too long! Please limit it to 255 characters.")
        return
    try:
        add_task(message.from_user.id, task)
        await message.reply(f"Task added successfully: '{task}' 👍")
    except Exception as e:
        await message.reply(f"Error adding task: {e}")

# Command: /list_tasks
async def cmd_list_tasks(message: types.Message):
    try:
        tasks = get_tasks(message.from_user.id)
        if not tasks:
            await message.reply("No tasks found. 🗒️ Use /add_task to create a new task.")
            return
        # Format tasks for better readability
        response = "\n".join(
            [f"{task['_id']}: {task['task']} {'✅' if task['completed'] else '❌'}" for task in tasks]
        )
        await message.reply(f"Here are your tasks:\n\n{response}")
    except Exception as e:
        await message.reply(f"Error retrieving tasks: {e}")

# Command: /complete_task
async def cmd_complete_task(message: types.Message):
    task_id = message.get_args()
    if not task_id or not task_id.isdigit():
        await message.reply("Please provide a valid numeric task ID! 🔢")
        return
    try:
        if mark_task_completed(message.from_user.id, int(task_id)):
            await message.reply(f"Task {task_id} has been marked as completed! ✅")
        else:
            await message.reply("Task not found or already completed! ❌")
    except Exception as e:
        await message.reply(f"Error completing task: {e}")

# Command: /edit_task
async def cmd_edit_task(message: types.Message):
    args = message.get_args().split(' ', 1)
    if len(args) < 2 or not args[0].isdigit():
        await message.reply("Please provide a valid task ID and new task description! Example: /edit_task 1 New Task Description")
        return

    task_id = int(args[0])
    new_task = args[1]

    if len(new_task) > 255:
        await message.reply("Task description is too long! Please limit it to 255 characters.")
        return

    try:
        if edit_task(message.from_user.id, task_id, new_task):
            await message.reply(f"Task {task_id} has been updated to: '{new_task}' 👍")
        else:
            await message.reply(f"Task {task_id} not found or cannot be updated. ❌")
    except Exception as e:
        await message.reply(f"Error editing task: {e}")

# Command: /remove_task
async def cmd_remove_task(message: types.Message):
    task_id = message.get_args()
    if not task_id or not task_id.isdigit():
        await message.reply("Please provide a valid task ID! 🔢")
        return

    try:
        if remove_task(message.from_user.id, int(task_id)):
            await message.reply(f"Task {task_id} has been removed! 🗑️")
        else:
            await message.reply(f"Task {task_id} not found or cannot be removed. ❌")
    except Exception as e:
        await message.reply(f"Error removing task: {e}")

# Register all handlers
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(cmd_add_task, commands=["add_task"])
    dp.register_message_handler(cmd_list_tasks, commands=["list_tasks"])
    dp.register_message_handler(cmd_complete_task, commands=["complete_task"])
    dp.register_message_handler(cmd_edit_task, commands=["edit_task"])
    dp.register_message_handler(cmd_remove_task, commands=["remove_task"])
