import asyncio
import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from layers.database.postgres.crud.user_repository import PostgresUserRepository


# Фікстура для mock callback
@pytest.fixture(scope="function")
def callback():
    mock_callback = AsyncMock()
    mock_callback.message.edit_text = AsyncMock()
    return mock_callback


# Фікстура для mock FSM state
@pytest.fixture(scope="function")
def state():
    mock_state = AsyncMock()
    mock_state.clear = AsyncMock()
    return mock_state


# Фікстура для асинхронної сесії SQLAlchemy
@pytest.fixture
async def async_session():
    mock_session = AsyncMock(spec=AsyncSession)
    yield mock_session


# Фікстура для репозиторію PostgresUserRepository
@pytest.fixture
def user_repository(async_session):
    mock_repo = AsyncMock(spec=PostgresUserRepository)
    mock_repo.session = async_session
    yield mock_repo


# Фікстура для управління базою даних (відкат змін після кожного тесту)
@pytest.fixture(scope="function", autouse=True)
async def setup_db(async_session):
    async with async_session.begin_nested():
        yield
        await async_session.rollback()
        await async_session.close()


# Загальна фікстура для створення event loop
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
