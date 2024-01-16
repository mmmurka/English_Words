import asyncio

import sqlalchemy.orm
from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from sqlalchemy.future import select


db_config = {
    "user": "mmmurka",
    "password": "12341",
    "host": "localhost",
    "database": "englishwords",
}

DATABASE_URL = f"postgresql+asyncpg://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

engine = create_async_engine(DATABASE_URL, echo=True)

Base = sqlalchemy.orm.declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)


'''func create_user(tg_user_id: int, name: str) -> None:'''


async def create_user(tg_user_id: int, name: str):
    async with AsyncSession(engine) as session:
        async with session.begin():
            user = User(id=tg_user_id, name=name)
            session.add(user)
        await session.commit()


async def main_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await create_user(54782134, "Steve Doe")



