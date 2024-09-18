import asyncio
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from layers.functions.common import shuffle_words
from layers.functions.cb_decoder import decode_table, decode_group_subject, decode_subject
from layers.functions.cb_encoder import encode_table, encode_group_subject, encode_subject
from modules.words.callbacks.f_data import send_bot_info, developers, button_back, word_tables, group_subject_fdata, \
    subjects_fdata, words_fdata
from layers.database.controller import database_module as db
from modules.words.data.data_retriever import get_words
from modules.words.keyboards import inline, builders
from modules.words.keyboards.paginators import create_group_subject_paginator, create_subject_paginator, \
    create_word_paginator


# мок калбека
@pytest.fixture(scope="function")
def callback():
    callback = AsyncMock()
    callback.message.edit_text = AsyncMock()
    return callback


# Мок фсм стейта
@pytest.fixture(scope="function")
def state():
    state = AsyncMock()
    state.clear = AsyncMock()
    return state


@pytest.fixture(scope="function", autouse=True)
async def setup_db(async_session):
    async with async_session.begin_nested():
        yield
        await async_session.rollback()
        await async_session.close()  # Явно закрываем сессию

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def async_session():
    async with AsyncSession(db.engine) as session:
        yield session


@pytest.mark.asyncio
async def test_send_bot_info_handler(callback):

    await send_bot_info(callback)
    #  assert_called_with -- assert that the last call was made with the specified arguments.
    callback.message.edit_text.assert_called_with(
        "Цей бот створенний для вивчення нових англійських слів по різним рівням,"
        " окремим темам чи по тестам, такі як: IELTS",
        reply_markup=inline.back_kb,
    )


@pytest.mark.asyncio
async def test_developers(callback):
    await developers(callback)

    callback.message.edit_text.assert_called_with(
        "Хей 🎭 ось розробники цього бота)\n\nПриємного користування! ☺️",
        reply_markup=inline.developers_kb,
    )


@pytest.mark.asyncio
async def test_button_back(callback, state):
    await button_back(callback, state)

    state.clear.assert_called_once()
    callback.message.edit_text.assert_called_with(
        f"Давай вивчати англійську разом 🇬🇧\n\n"
        f"Ти можеш обрати розділ з необхідними темами, або вивчати нові слова на своєму рівні\n\n\n"
        f"Keep going! \n\n"
        f"⬇️Обери необхідний пункт нижче⬇️\n",
        reply_markup=builders.greeting_kb(),
    )


@pytest.mark.asyncio
async def test_word_tables(callback):
    await word_tables(callback)

    callback.message.edit_text.assert_called_with(
        "Супер!🥳 \n\nДавай оберемо розділ для вивчення слів💫",
        reply_markup=builders.word_tables_kb(),
    )


@pytest.mark.asyncio
async def test_group_subject_fdata(callback):

    encoded_table = encode_table('topic_vocabulary')
    callback.data = f'group_subject:{encoded_table}:2'
    paginator = await create_group_subject_paginator(encoded_table)
    await group_subject_fdata(callback)

    callback.message.edit_text.assert_called_with("Оберіть тему:", reply_markup=paginator(2))


@pytest.mark.asyncio
async def test_subjects_fdata(callback, state):

    encoded_table = encode_table('topic_vocabulary')
    encoded_group_subject = encode_group_subject('animals')
    callback.data = f'subjects:{encoded_table}:{encoded_group_subject}:0:0'
    paginator = await create_subject_paginator(encoded_table, encoded_group_subject, 0)
    await subjects_fdata(callback, state)

    state.clear.assert_called_once()

    callback.message.edit_text.assert_called_with("Оберіть тему:", reply_markup=paginator(0))


@pytest.mark.asyncio
async def test_words_fdata(callback, state):
    encoded_table = encode_table('topic_vocabulary')
    encoded_group_subject = encode_group_subject('animals')
    encoded_subject = encode_subject('1 - large mammals')

    callback.data = f'words:{encoded_table}:{encoded_group_subject}:{encoded_subject}:0:0:0'

    paginator = await create_word_paginator(encoded_table, encoded_group_subject, encoded_subject, state, 0, 0)

    await words_fdata(callback, state)

    words, definitions = await get_words(
        decode_table(encoded_table),
        decode_group_subject(encoded_group_subject),
        decode_subject(encoded_subject),
    )
    words, definitions = shuffle_words(words, definitions)

    callback.message.edit_text.assert_called_with(
        f"{words[0]} - {definitions[0]}", reply_markup=paginator()
    )