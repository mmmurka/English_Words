import time
from re import search

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Telegram.data import database_module as db
import asyncio


async def topic_from_table(table_name):
    async with AsyncSession(db.engine) as session:
        async with session.begin():
            table = db.create_table_class(table_name)
            stmt = select(table.group_subject).distinct()
            result = await session.execute(stmt)
            unique_values = result.scalars().all()
            return unique_values


async def theme_from_topic(table_name, group_subject):
    async with AsyncSession(db.engine) as session:
        async with session.begin():
            table_name = table_name.lower()

            table = db.create_table_class(table_name)
            stmt = select(table.subject).distinct().where(table.group_subject == group_subject).group_by(table.id)
            result = await session.execute(stmt)
            unique_values = result.scalars().all()
            values = [i.replace('   ', ' ') for i in unique_values]
            values = sorted(values, key=lambda x: int(search(r'\d+', x).group()))
            return values

if __name__ == '__main__':
    asyncio.run(theme_from_topic('english by level', 'C1 Level Wordlist'))