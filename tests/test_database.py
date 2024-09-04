import pytest
from alembic import command
from alembic.config import Config
import os

from sqlalchemy.ext.asyncio import create_async_engine


from layers.database.models import User
from layers.database.functions.create_user_ import create_user
from sqlalchemy.future import select
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL_TEST")
engine = create_async_engine(DATABASE_URL, echo=True)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    os.environ["DB_URL"] = os.getenv("MIGRATE_URL_TEST")

    alembic_cfg = Config("alembic.ini")

    # Upgrade the database
    command.upgrade(alembic_cfg, "head")

    yield


@pytest.mark.asyncio
async def test_create_user_success(setup_test_db):
    tg_user_id = 612321331346
    name = "Goga Nemsk"
    username = "goga.nemsk"

    await create_user(tg_user_id, name, username, engine)

    async with engine.begin() as conn:
        result = await conn.execute(select(User).where(User.id == tg_user_id))
        user = result.fetchone()

    assert user is not None
    assert user.name == name
    assert user.username == username

    await engine.dispose()


@pytest.mark.asyncio
async def test_create_no_username(setup_test_db):
    tg_user_id = 232313
    name = "Rodrigaz"
    username: None = None

    await create_user(tg_user_id, name, username, engine)

    async with engine.begin() as conn:
        result = await conn.execute(select(User).where(User.id == tg_user_id))
        user = result.fetchone()

    assert user is not None, "User was not created"
    assert user.name == name, "User name does not match"
    assert user.username is None, "Username should be None"

    await engine.dispose()
