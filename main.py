import asyncio

import logging
from aiogram import Bot, Dispatcher
from config.config import lock_path
from aiogram.fsm.storage.memory import MemoryStorage
import fasteners
import os
from dotenv import load_dotenv

from modules.words.handlers import bot_messages, user_commands, pagination_handlers
from modules.words.callbacks import f_data

lock = fasteners.InterProcessLock(lock_path)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",)
load_dotenv()


async def main():
    bot = Bot(os.getenv('TELEGRAM_TOKEN'))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(
        pagination_handlers.router,
        user_commands.router,
        bot_messages.router,
        f_data.router
    )

    with lock:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
