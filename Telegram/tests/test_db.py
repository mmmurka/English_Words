import pytest
import logging
from sqlalchemy.future import select
from Telegram.data.database_module import Base, User, engine, create_user

# Configure logging
logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
async def setup_database():
    logging.debug("Setting up database")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    logging.debug("Tearing down database")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_user(setup_database):
    tg_user_id = 24421
    name = "Art Nemsk"

    logging.debug("Creating user")
    await create_user(tg_user_id, name)

    logging.debug("Querying user from the database")
    async with engine.begin() as conn:
        result = await conn.execute(select(User).where(User.id == tg_user_id))
        user = result.fetchone()

    logging.debug("Checking assertions")
    assert user is not None, "User not found in the database"
    assert user.name == name, f"Expected user name to be '{name}', but got '{user.name}'"
