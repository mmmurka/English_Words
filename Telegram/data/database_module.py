import asyncio

import sqlalchemy.orm
from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from dotenv import load_dotenv
import os


load_dotenv()

db_config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_DATABASE"),
}

DATABASE_URL = f"postgresql+asyncpg://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

engine = create_async_engine(DATABASE_URL, echo=True)

Base = sqlalchemy.orm.declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)


def create_table_class(tablename, extend_existing=True):
    """Leave the metadata as is, it will be used in other files
    Don't change metadata.tables[tablename] = Table
    """
    class Table(Base):
        __tablename__ = tablename
        __table_args__ = {'extend_existing': True}

        id = Column(BigInteger, primary_key=True)
        group_subject = Column(String)
        subject = Column(String)
        word = Column(String)
        definition = Column(String)

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
