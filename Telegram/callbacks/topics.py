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
            table = db.create_table_class(table_name)
            stmt = select(table.subject).distinct().where(table.group_subject == group_subject).group_by(table.id)
            result = await session.execute(stmt)
            unique_values = result.scalars().all()
            values = [i.replace('   ', ' ') for i in unique_values]
            values = sorted(values, key=lambda x: int(search(r'\d+', x).group()))
            return values

async def words_from_theme(table_name, theme_word):
    async with AsyncSession(db.engine) as session:
        async with session.begin():
            result = {}
            table = db.create_table_class(table_name)
            stmt = select(table.word).where(table.subject.like(f'%{theme_word}%')).group_by(table.id)
            words = await session.execute(stmt)
            words = words.scalars().all()
            stmt = select(table.definition).where(table.subject.like(f'%{theme_word}%')).group_by(table.id)
            definitions = await session.execute(stmt)
            definitions = definitions.scalars().all()
            for i in range(0,len(words)-1):
                result[words[i]] = definitions[i]
            return result

if __name__ == '__main__':
    asyncio.run(words_from_theme('english by level',  'Hello and Goodbye'))