from unittest.mock import AsyncMock, patch

import pytest
from aiogram.fsm.context import FSMContext
from layers.functions.cb_encoder import encode_table
from modules.words.callbacks.f_data import send_bot_info, developers, button_back, word_tables, group_subject_fdata
from modules.words.keyboards import inline, builders
from modules.words.keyboards.paginators import create_group_subject_paginator


# Пример фикстуры для мокирования CallbackQuery
@pytest.fixture
def callback():
    callback = AsyncMock()
    callback.message.edit_text = AsyncMock()
    return callback


# Пример фикстуры для мокирования FSMContext
@pytest.fixture
def state():
    return AsyncMock(FSMContext)


@pytest.mark.asyncio
async def test_send_bot_info_handler(callback):
    # Вызываем обработчик
    await send_bot_info(callback)

    # Проверяем, что edit_text был вызван с правильным текстом и reply_markup
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


# @pytest.mark.asyncio
# async def test_group_subject_fdata(callback):
#     # Подготавливаем данные
#     encoded = encode_table('topic_vocabulary')  # Подмените это на правильный зашифрованный формат, если у вас есть кодирование
#     callback.data = f'group_subject:{encoded}:2'
#     paginator = AsyncMock()
#
#     # Используем patch для замены функции create_group_subject_paginator
#     with patch('modules.words.keyboards.paginators.create_group_subject_paginator', return_value=paginator) as mock_paginator:
#         await group_subject_fdata(callback)
#
#         # Проверка, что функция пагинации была вызвана
#         mock_paginator.assert_called_once_with(encoded)
#
#         # Проверка, что пагинатор был вызван с правильной страницей
#         paginator.assert_called_once_with(2)
#
#         # Проверка, что сообщение было отредактировано с правильным текстом и клавиатурой
#         callback.message.edit_text.assert_called_with("Оберіть тему:", reply_markup=paginator(2))
