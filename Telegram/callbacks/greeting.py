from contextlib import suppress

from aiogram import Router, F
from aiogram.types import CallbackQuery
from Telegram.keyboards import fabrics, inline
from Telegram.translate.translateAPI import trans_text


router = Router()


@router.callback_query(F.data == "devs")
async def send_info_devs(callback: CallbackQuery):
    await callback.message.edit_text('Хей 🎭 ось розробники цього бота)\n\nПриємного користування! ☺️',
                                     reply_markup=inline.linsk_kb)


@router.callback_query(F.data == "bot_info")
async def send_bot_info(callback: CallbackQuery):
    await callback.message.edit_text('Цей бот створенний для вивчення нових англійських слів по різним рівням, окремим темам чи по тестам, такі як: IELTS',
                                     reply_markup=inline.back_kb)


@router.callback_query(F.data == "back")
async def button_back(callback: CallbackQuery):
    await callback.message.edit_text(
        f'Давай вивчати англійську разом 🇬🇧\n\n'
        f'Ти можеш обрати розділ з необхідними темами, або вивчати нові слова на своєму рівні\n\n\n'
        f'Keep going! \n\n'
        f'⬇️Обери необхідний пункт нижче⬇️\n',
                         reply_markup=fabrics.greeting())


@router.callback_query(F.data == "topics")
async def topics(callback: CallbackQuery):
    await callback.message.edit_text('Comming soon...            ⠀', reply_markup=inline.back_kb)


@router.callback_query(F.data == "support")
async def support(callback: CallbackQuery):
    word = await trans_text(text='Hello', src='en', dest='uk')
    await callback.message.edit_text(f'translate: {word}', reply_markup=inline.back_kb)
