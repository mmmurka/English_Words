import asyncio
from contextlib import suppress

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from config import telegram_token, lock_path
import fasteners
import keyboards


bot = Bot(telegram_token, parse_mode='HTML')
dp = Dispatcher()

smiles = [
    ['⚓️', 'Якорь поднять, паруса опустить!'],
    ['🌽', 'Это что, отсылка на Хрущева?'],
    ['🦈', 'Акула не карась, страус не птица'],
    ['🏹', 'Расскажи как ты на миду раздал']
]

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Hello, {message.from_user.first_name}',
                         reply_markup=keyboards.main_kb)

@dp.callback_query(keyboards.Pagination.filter(F.action.in_(["prev", "next"])))
async def pagination_handler(call: CallbackQuery, callback_data: keyboards.Pagination):
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == "next":
        page = page_num + 1 if page_num < (len(smiles) - 1) else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f"{smiles[page][0]} <b>{smiles[page][1]}</b>",
            reply_markup=keyboards.paginator(page)
        )
    await call.answer('тут текст)')

@dp.message()
async def echo(message: Message):
    msg = message.text.lower()

    if msg == 'ссылки':
        await message.answer('Вот ваши ссылки:', reply_markup=keyboards.linsk_kb)
    elif msg == 'спец кнопки':
        await message.answer("Вот спец кнопки", reply_markup=keyboards.spec_kb)
    elif msg == 'калькулятор':
        await message.answer('Введите выражение:', reply_markup=keyboards.calc_kb())
    elif msg == 'смайлики':
        await message.answer(f'{smiles[0][0]} <b>{smiles[0][1]}</b>', reply_markup=keyboards.paginator())# в аргументы функции ничего не передается, так как по дефолту там стоит 0



lock = fasteners.InterProcessLock(lock_path)
async def main():
    with lock:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


if __name__ =='__main__':
    asyncio.run(main())