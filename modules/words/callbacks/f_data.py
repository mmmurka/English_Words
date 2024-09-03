from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from layers.functions.cb_decoder import decode_table, decode_group_subject
from modules.words.data.data_retriever import get_group_subjects
from modules.words.keyboards.paginators import create_subject_paginator, Pagination
from modules.words.keyboards import inline

router = Router()


@router.callback_query(F.data == "developers")
async def developers(callback: CallbackQuery):
    await callback.message.edit_text('Хей 🎭 ось розробники цього бота)\n\nПриємного користування! ☺️',
                                     reply_markup=inline.developers_kb)


@router.callback_query(F.data == "bot_info")
async def send_bot_info(callback: CallbackQuery):
    await callback.message.edit_text(
        'Цей бот створенний для вивчення нових англійських слів по різним рівням, окремим темам чи по тестам, такі як: IELTS',
        reply_markup=inline.back_kb)


@router.callback_query(F.data == "back")
async def button_back(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        f'Давай вивчати англійську разом 🇬🇧\n\n'
        f'Ти можеш обрати розділ з необхідними темами, або вивчати нові слова на своєму рівні\n\n\n'
        f'Keep going! \n\n'
        f'⬇️Обери необхідний пункт нижче⬇️\n',
        reply_markup=inline.greeting_kb())

@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery) -> None:
    await callback.message.edit_text('Ваш профіль', reply_markup=inline.profile_kb)


@router.callback_query(F.data == "word_tables")
async def word_tables(callback: CallbackQuery):
    await callback.message.edit_text('Супер!🥳 \n\nДавай оберемо розділ для вивчення слів💫',
                                     reply_markup=inline.word_tables_kb())

@router.callback_query(F.data.startswith('group_subject:'))
async def group_subject(callback: CallbackQuery):
    table_name = callback.data.split(':')[1]
    paginator = await create_subject_paginator(table_name)
    await callback.message.edit_text("Оберіть тему:", reply_markup=paginator())


# @router.callback_query(F.data.startswith('subjects:'))
# async def subjects(callback: CallbackQuery, state: FSMContext):
#     await state.clear()
#     button_info = callback.data.split(':')
#     table_name = decode_table(button_info[1])
#     group_subject = decode_group_subject(button_info[2])
#     paginator = await subject_paginator(' '.join(table_name), ' '.join(group_subject), 'subjects')
#
#     await callback.message.edit_text("Оберіть розділ:", reply_markup=paginator(0))

