from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from modules.english_words.keyboards import fabrics
from functions.create_user_ import create_user

router = Router()


@router.message(CommandStart())
async def start(message: Message):

    tg_user_id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username

    await create_user(tg_user_id, name, username)

    await message.answer(
        f'{name}, привітики!🙈\n\nДавай вивчати англійську разом 🇬🇧\n\n'
        f'Ти можеш обрати розділ з необхідними темами, або вивчати нові слова на своєму рівні\n\n\n'
        f'Keep going! \n\n'
        f'⬇️Обери необхідний пункт нижче⬇️\n', reply_markup=fabrics.greeting())
