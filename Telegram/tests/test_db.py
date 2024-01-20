import pytest
from sqlalchemy.future import select
from Telegram.data.database_module import Base, User, engine, create_user


@pytest.fixture
async def setup_database():
    print("Setting up database")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("Tearing down database")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_user(setup_database):
    tg_user_id = 61232346
    name = "Goga Nemsk"

    print("Creating user")
    await create_user(tg_user_id, name)

    print("Querying user from the database")
    async with engine.begin() as conn:
        result = await conn.execute(select(User).where(User.id == tg_user_id))
        user = result.fetchone()

    print("Checking assertions")
    assert user is not None, "User not found in the database"
    assert user.name == name, f"Expected user name to be '{name}', but got '{user.name}'"