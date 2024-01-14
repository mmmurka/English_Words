from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from Telegram.keyboards import reply

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Hello, {message.from_user.first_name}',
                         reply_markup=reply.main_kb)

