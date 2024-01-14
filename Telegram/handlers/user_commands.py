import asyncio

from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from sqlalchemy.future import select


from Telegram.keyboards import reply
from Telegram.data import database_module as db

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
            await message.reply("User already exists in the database.")
        else:
            await db.create_user(tg_user_id, name)
            await message.reply(f"User {name} with ID {tg_user_id} added to the database.")


    cat = FSInputFile("cat.jpg")
    await message.answer(f'{message.from_user.first_name}, {message.from_user.id}, привітики')
    await asyncio.sleep(0.5)
    await message.answer_photo(cat)
    await asyncio.sleep(0.3)
    await message.answer('Я бот піськін-гризкінь, давай разом вивчати англійську, обери свій варіант',
                         reply_markup=reply.main_kb)
