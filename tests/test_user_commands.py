import pytest
from unittest.mock import AsyncMock
from aiogram import types
from modules.words.handlers.user_commands import start
from modules.words.keyboards.builders import greeting_kb


@pytest.fixture
def create_message():
    def _create_message(user_id, first_name, username):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.from_user = AsyncMock()
        message.from_user.id = user_id
        message.from_user.first_name = first_name
        message.from_user.username = username
        return message

    return _create_message


@pytest.fixture
def expected_message():
    def _expected_message(first_name):
        return (
            f"{first_name}, привітики!🙈\n\nДавай вивчати англійську разом 🇬🇧\n\n"
            "Ти можеш обрати розділ з необхідними темами, або вивчати нові слова на своєму рівні\n\n\n"
            "Keep going! \n\n⬇️Обери необхідний пункт нижче⬇️\n"
        )

    return _expected_message


@pytest.mark.asyncio
async def test_start_command(user_repository, create_message, expected_message):
    user_id = 12345
    first_name = "John"
    username = "john_doe"

    message = create_message(user_id, first_name, username)

    await start(message, user_repository)
    user_repository.create_user.assert_called_once_with(user_id, first_name, username)
    message.answer.assert_called_once_with(expected_message(first_name), reply_markup=greeting_kb())


@pytest.mark.asyncio
async def test_start_command_empty_first_name(user_repository, create_message, expected_message):
    user_id = 12345
    first_name = ""
    username = "john_doe"

    message = create_message(user_id, first_name, username)

    await start(message, user_repository)
    user_repository.create_user.assert_called_once_with(user_id, first_name, username)
    message.answer.assert_called_once_with(expected_message(first_name), reply_markup=greeting_kb())
