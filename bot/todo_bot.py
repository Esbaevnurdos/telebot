from aiogram import Bot, Dispatcher, executor, types
from bot.handlers import register_handlers
import os
# from bot.handlers import register_handlers


API_TOKEN = os.getenv("BOT_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Register command handlers
register_handlers(dp)

if __name__ == "__main__":
    print("Starting bot...")
    executor.start_polling(dp, skip_updates=True)
