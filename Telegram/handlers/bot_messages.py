from aiogram import Router
from aiogram.types import Message

from keyboards import builders, fabrics, inline, reply
from data.subloader import get_json

router = Router()

@router.message()
async def echo(message: Message):
    msg = message.text.lower()
    smiles = await get_json('smiles.json')

    if msg == 'ссылки':
        await message.answer('Вот ваши ссылки:', reply_markup=inline.linsk_kb)
    elif msg == 'спец кнопки':
        await message.answer("Вот спец кнопки", reply_markup=reply.spec_kb)
    elif msg == 'калькулятор':
        await message.answer('Введите выражение:', reply_markup=builders.calc_kb())
    elif msg == 'смайлики':
        await message.answer(f'{smiles[0][0]} <b>{smiles[0][1]}</b>', reply_markup=fabrics.paginator())# в аргументы функции ничего не передается, так как по дефолту там стоит 0