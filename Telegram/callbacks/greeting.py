from contextlib import suppress

from aiogram import Router, F
from aiogram.types import CallbackQuery
from Telegram.keyboards import fabrics, inline


router = Router()


@router.callback_query(F.data == "topics")
async def send_random_value(callback: CallbackQuery):
    await callback.message.edit_text('Comming soon...            ⠀', reply_markup=inline.linsk_kb)


@router.callback_query(F.data == "devs")
async def send_random_value(callback: CallbackQuery):
    await callback.message.edit_text('Хей 🎭 ось розробники цього бота)\n\nПриємного користування! ☺️',
                                     reply_markup=inline.linsk_kb)


@router.callback_query(F.data == "back")
async def send_random_value(callback: CallbackQuery):
    await callback.message.edit_text(
        f'Давай вивчати англійську разом 🇬🇧\n\n'
        f'Ти можеш обрати розділ з необхідними темами, або вивчати нові слова на своєму рівні\n\n\n'
        f'Keep going! \n\n'
        f'⬇️Обери необхідний пункт нижче⬇️\n',
                         reply_markup=fabrics.greeting())