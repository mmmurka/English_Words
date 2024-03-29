import asyncio
from contextlib import suppress

from aiogram import Router, F, types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Telegram.keyboards import fabrics, inline
from Telegram.keyboards.builders import topic_kb, theme_kb
from Telegram.keyboards.inline import trans_kb
from Telegram.translate.translateAPI import trans_text
from Telegram.utils.states import Form
from aiogram.utils.keyboard import InlineKeyboardBuilder
from Telegram.callbacks.topics import topic_from_table, theme_from_topic, words_from_theme, group_from_theme
from Telegram.keyboards.fabrics import create_paginator, create_theme_paginator
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.callback_query(F.data == "devs")
async def send_info_devs(callback: CallbackQuery):
    await callback.message.edit_text('Хей 🎭 ось розробники цього бота)\n\nПриємного користування! ☺️',
                                     reply_markup=inline.linsk_kb)


@router.callback_query(F.data == "bot_info")
async def send_bot_info(callback: CallbackQuery):
    await callback.message.edit_text(
        'Цей бот створенний для вивчення нових англійських слів по різним рівням, окремим темам чи по тестам, такі як: IELTS',
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
    await callback.message.edit_text('Супер!🥳 \n\nДавай оберемо розділ для вивчення слів💫',
                                     reply_markup=inline.topics_kb)


@router.callback_query(F.data == "translate")
async def support(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text('Оберіть мову перекладу :)', reply_markup=trans_kb)


@router.callback_query(F.data == "ukraine")
async def ukr_trans(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.word)
    await callback.message.edit_text(
        'Напишіть слово для перекладу ')


@router.callback_query(F.data == "english")
async def eng_trans(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.slovo)
    await callback.message.edit_text(
        'Напишіть слово для перекладу ')


@router.callback_query(F.data.startswith('topic:'))
async def topic(callback: CallbackQuery, state: FSMContext):
    button_info = callback.data.split(':')
    table = button_info[1].split('_')
    topics_list = await topic_from_table(' '.join(table))
    my_paginator = await create_theme_paginator(' '.join(table), ' ', 'topic')
    await callback.message.edit_text("Оберіть тему:", reply_markup=my_paginator(0))


@router.callback_query(F.data.startswith('theme:'))
async def theme(callback: CallbackQuery, state: FSMContext):
    button_info = callback.data.split(':')
    group_subject = button_info[2].split('_')
    table = button_info[1].split('_')
    # themes_list = await theme_from_topic(' '.join(table), ' '.join(group_subject))
    # keyboard = theme_kb(themes_list, '_'.join(table), '_'.join(group_subject))
    my_paginator = await create_theme_paginator(' '.join(table), ' '.join(group_subject), 'theme')
    await callback.message.edit_text("Оберіть тему:", reply_markup=my_paginator(0))


@router.callback_query(F.data.startswith('words:'))
async def words(callback: CallbackQuery, state: FSMContext):
    button_info = callback.data.split(':')
    table = button_info[1].split("_")
    theme = button_info[2].split("_")
    word_definition = await words_from_theme(' '.join(table), ' '.join(theme))
    my_paginator = await create_paginator(button_info[1], button_info[2])
    await callback.message.edit_text(f'{word_definition[0]}', reply_markup=my_paginator())
