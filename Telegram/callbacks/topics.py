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
