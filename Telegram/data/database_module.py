import asyncio
import enum

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


def create_table_class(tablename, extend_existing=True):
    class Table(Base):
        __tablename__ = tablename
        __table_args__ = {'extend_existing': True}

        id = Column(BigInteger, primary_key=True)
        group_subject = Column(String)
        subject = Column(String)
        word = Column(String)
        definition = Column(String)

    # Оставьте метаданные как они есть, они будут использоваться в других файлах
    # Не изменяйте metadata.tables[tablename] = Table

    return Table


async def create_user(tg_user_id: int, name: str):
    async with AsyncSession(engine) as session:
        async with session.begin():
            user = User(id=tg_user_id, name=name)
            session.add(user)
        await session.commit()


async def main_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await create_user(3141592658979, "John Doe")


if __name__ == '__main__':
    asyncio.run(main_db())
