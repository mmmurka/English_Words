from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from layers.functions.cb_decoder import (
    decode_table,
    decode_group_subject,
    decode_subject,
)
from layers.functions.common import shuffle_words
from modules.words.data.data_retriever import get_words
from modules.words.keyboards.paginators import (
    create_group_subject_paginator,
    create_subject_paginator,
    create_word_paginator,
)

from modules.words.keyboards import inline, builders

router = Router()


@router.callback_query(F.data == "developers")
async def developers(callback: CallbackQuery):
    await callback.message.edit_text(
        "Хей 🎭 ось розробники цього бота)\n\nПриємного користування! ☺️",
        reply_markup=inline.developers_kb,
    )


@router.callback_query(F.data == "bot_info")
async def send_bot_info(callback: CallbackQuery):
    await callback.message.edit_text(
        "Цей бот створенний для вивчення нових англійських слів по різним рівням,"
        " окремим темам чи по тестам, такі як: IELTS",
        reply_markup=inline.back_kb,
    )


@router.callback_query(F.data == "back")
async def button_back(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        f"Давай вивчати англійську разом 🇬🇧\n\n"
        f"Ти можеш обрати розділ з необхідними темами, або вивчати нові слова на своєму рівні\n\n\n"
        f"Keep going! \n\n"
        f"⬇️Обери необхідний пункт нижче⬇️\n",
        reply_markup=builders.greeting_kb(),
    )


@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Ваш профіль", reply_markup=inline.profile_kb)


@router.callback_query(F.data == "word_tables")
async def word_tables(callback: CallbackQuery):
    await callback.message.edit_text(
        "Супер!🥳 \n\nДавай оберемо розділ для вивчення слів💫",
        reply_markup=builders.word_tables_kb(),
    )


@router.callback_query(F.data.startswith("group_subject:"))
async def group_subject(callback: CallbackQuery):
    table_name = callback.data.split(":")[1]
    paginator = await create_group_subject_paginator(table_name)
    await callback.message.edit_text("Оберіть тему:", reply_markup=paginator())


@router.callback_query(F.data.startswith("subjects:"))
async def subjects(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    table_name = callback.data.split(":")[1]
    group_subject = callback.data.split(":")[2]
    paginator = await create_subject_paginator(table_name, group_subject)
    await callback.message.edit_text("Оберіть тему:", reply_markup=paginator())


@router.callback_query(F.data.startswith("words:"))
async def words(callback: CallbackQuery, state: FSMContext):
    table_name = callback.data.split(":")[1]
    group_subject = callback.data.split(":")[2]
    subject = callback.data.split(":")[3]
    words, definitions = await get_words(
        decode_table(table_name),
        decode_group_subject(group_subject),
        decode_subject(subject),
    )
    words, definitions = shuffle_words(words, definitions)
    await state.update_data(words=words, definitions=definitions)
    paginator = await create_word_paginator(table_name, group_subject, subject, state)
    await callback.message.edit_text(
        f"{words[0]} - {definitions[0]}", reply_markup=paginator()
    )
