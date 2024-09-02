import asyncio
from layers.database.controller.database_module import engine, Base
from create_user_ import create_user


async def main_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await create_user(3141592658979, "John Doe", "johndoe")


if __name__ == '__main__':
    asyncio.run(main_db())
