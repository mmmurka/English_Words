import asyncio

import logging
from aiogram import Bot, Dispatcher
from config.config import lock_path
from aiogram.fsm.storage.memory import MemoryStorage
import fasteners
import os
from dotenv import load_dotenv

from modules.english_words.handlers import questionaire
from modules.english_words.handlers import user_commands, bot_messages
from modules.english_words.callbacks import pagination, greeting

#lock = fasteners.InterProcessLock(lock_path)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",)
load_dotenv()


async def main():
    bot = Bot(os.getenv('TELEGRAM_TOKEN'), parse_mode='HTML')
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(
        user_commands.router,
        pagination.router,
        questionaire.router,
        bot_messages.router,
        greeting.router
    )


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
