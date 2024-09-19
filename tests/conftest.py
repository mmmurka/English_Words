import asyncio
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from layers.database.controller import database_module as db


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
