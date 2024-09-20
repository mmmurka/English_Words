import pytest
from unittest.mock import AsyncMock, patch
from aiogram import types
from modules.words.handlers.user_commands import start
from modules.words.keyboards.builders import greeting_kb


@pytest.mark.asyncio
@patch("layers.database.functions.create_user_.create_user")
async def test_start_command(mock_create_user):
    user_id = 12345
    first_name = "John"
    username = "john_doe"
    expected_message = (
        f"{first_name}, привітики!🙈\n\nДавай вивчати англійську разом 🇬🇧\n\n"
        "Ти можеш обрати розділ з необхідними темами, або вивчати нові слова на своєму рівні\n\n\n"
        "Keep going! \n\n⬇️Обери необхідний пункт нижче⬇️\n"
    )

    message = AsyncMock(spec=types.Message)
    message.answer = AsyncMock()
    message.from_user = AsyncMock()
    message.from_user.id = user_id
    message.from_user.first_name = first_name
    message.from_user.username = username

    await start(message)
    await mock_create_user(user_id, first_name, username)
    mock_create_user.assert_called_once_with(user_id, first_name, username)

    message.answer.assert_called_once_with(expected_message, reply_markup=greeting_kb())


@pytest.mark.asyncio
@patch("layers.database.functions.create_user_.create_user")
async def test_start_command_empty_first_name(mock_create_user):
    user_id = 12345
    first_name = ""
    username = "john_doe"
    expected_message = (
        f", привітики!🙈\n\nДавай вивчати англійську разом 🇬🇧\n\n"
        "Ти можеш обрати розділ з необхідними темами, або вивчати нові слова на своєму рівні\n\n\n"
        "Keep going! \n\n⬇️Обери необхідний пункт нижче⬇️\n"
    )

    message = AsyncMock(spec=types.Message)
    message.answer = AsyncMock()
    message.from_user = AsyncMock()
    message.from_user.id = user_id
    message.from_user.first_name = first_name
    message.from_user.username = username

    await start(message)
    await mock_create_user(user_id, first_name, username)
    mock_create_user.assert_called_once_with(user_id, first_name, username)

    message.answer.assert_called_once_with(expected_message, reply_markup=greeting_kb())
