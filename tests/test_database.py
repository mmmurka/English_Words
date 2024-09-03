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

DATABASE_URL = os.getenv('DATABASE_URL_TEST')
engine = create_async_engine(DATABASE_URL, echo=True)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    os.environ['DB_URL'] = os.getenv('MIGRATE_URL_TEST')

    alembic_cfg = Config("alembic.ini")

    # Upgrade the database
    command.upgrade(alembic_cfg, "head")

    yield


@pytest.mark.asyncio
async def test_create_user(setup_test_db):
    tg_user_id = 612321331346
    name = "Goga Nemsk"
    username = 'goga.nemsk'

    print("Creating user")
    await create_user(tg_user_id, name, username, engine)

    print("Querying user from the database")
    async with engine.begin() as conn:
        result = await conn.execute(select(User).where(User.id == tg_user_id))
        user = result.fetchone()

    print("Checking assertions")
    assert user is not None, "User not found in the database"
    assert user.name == name, f"Expected user name to be '{name}', but got '{user.name}'"