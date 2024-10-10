import asyncio
import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession


# Фикстура для mock callback
@pytest.fixture(scope="function")
def callback():
    mock_callback = AsyncMock()
    mock_callback.message.edit_text = AsyncMock()
    return mock_callback


# Фикстура для mock FSM state
@pytest.fixture(scope="function")
def state():
    mock_state = AsyncMock()
    mock_state.clear = AsyncMock()
    return mock_state


# Фикстура для управления базой данных (откат изменений после каждого теста)
@pytest.fixture(scope="function", autouse=True)
async def setup_db(async_session):
    async with async_session.begin_nested():
        yield
        await async_session.rollback()
        await async_session.close()


# Общая фикстура для создания event loop
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Фикстура для асинхронной сессии SQLAlchemy
@pytest.fixture
async def async_session():
    async with AsyncSession(db.engine) as session:
        yield session
