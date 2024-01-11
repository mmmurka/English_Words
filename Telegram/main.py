import asyncio

from aiogram import Bot, Dispatcher
from config import telegram_token, lock_path
import fasteners

from handlers import bot_messages, user_commands
from callbacks import pagination


lock = fasteners.InterProcessLock(lock_path)


async def main():
    bot = Bot(telegram_token, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
        pagination.router,
        bot_messages.router
    )


    with lock:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())