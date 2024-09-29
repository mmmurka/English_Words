from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from modules.words.keyboards.builders import greeting_kb
from layers.database1.postgres.crud.user_repository import PostgresUserRepository
from layers.database1.postgres.controller.database import DBManager


router = Router()
db_manager = DBManager()
user_repository = PostgresUserRepository(db_manager.getSession)


@router.message(CommandStart())
async def start(message: Message):
    tg_user_id: int = message.from_user.id
    name: str = message.from_user.first_name
    username: str = message.from_user.username

    await user_repository.create_user(tg_user_id, name, username)

    await message.answer(
        f"{name}, привітики!🙈\n\nДавай вивчати англійську разом 🇬🇧\n\n"
        f"Ти можеш обрати розділ з необхідними темами, або вивчати нові слова на своєму рівні\n\n\n"
        f"Keep going! \n\n"
        f"⬇️Обери необхідний пункт нижче⬇️\n",
        reply_markup=greeting_kb(),
    )
