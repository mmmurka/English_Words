import asyncio

import logging
from aiogram import Bot, Dispatcher
from config import telegram_token, lock_path
import fasteners

from handlers import bot_messages, user_commands, questionaire
from callbacks import pagination

lock = fasteners.InterProcessLock(lock_path)
logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(telegram_token, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
        pagination.router,
        questionaire.router,
        bot_messages.router
    )

    with lock:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
