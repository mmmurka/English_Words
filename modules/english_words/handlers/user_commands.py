from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.future import select


from modules.english_words.keyboards import fabrics
from layers.database.controller import database_module as db

router = Router()


@router.message(CommandStart())
async def start(message: Message):

    tg_user_id = message.from_user.id
    name = message.from_user.first_name

    async with db.AsyncSession(db.engine) as session:
        stmt = select(db.User).filter(db.User.id == tg_user_id)
        result = await session.execute(stmt)
        existing_user = result.scalar()

        if existing_user:
            print(f'User {name} already exists in the database.')

        else:
            await db.create_user(tg_user_id, name)
            print(f'User {name} with ID {tg_user_id} added to the database.')

    await message.answer(
        f'{name}, привітики!🙈\n\nДавай вивчати англійську разом 🇬🇧\n\n'
        f'Ти можеш обрати розділ з необхідними темами, або вивчати нові слова на своєму рівні\n\n\n'
        f'Keep going! \n\n'
        f'⬇️Обери необхідний пункт нижче⬇️\n', reply_markup=fabrics.greeting())
