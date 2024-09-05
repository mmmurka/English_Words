from typing import Type

from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from layers.database.controller import database_module as db
from layers.database.models import DynamicTable


# Функция для создания динамического класса, который будет представлять таблицу
def get_dynamic_table_class(table_name: str) -> Type[DynamicTable]:
    class TableClass(DynamicTable):
        __tablename__ = table_name
        __table_args__ = {'extend_existing': True}  # Указываем, что таблица уже существует

    return TableClass


async def get_group_subjects(table_name: str):
    TableClass = get_dynamic_table_class(table_name)
    stmt = select(distinct(TableClass.group_subject))

    async with AsyncSession(db.engine) as session:
        async with session.begin():
            result = await session.execute(stmt)
            group_subject_list = result.scalars().all()
            return sorted(group_subject_list)


async def get_subjects(table_name: str, group_subject: str):
    group_subject = group_subject.replace('_', ' ')
    TableClass = get_dynamic_table_class(table_name)
    stmt = select(distinct(TableClass.subject)).where(TableClass.group_subject == group_subject)

    async with AsyncSession(db.engine) as session:
        async with session.begin():
            result = await session.execute(stmt)
            subject_list = result.scalars().all()
            return sorted(subject_list, key=lambda x: int(x.split('-')[0].strip()))


async def get_words(table_name: str, group_subject: str, subject: str):
    group_subject = group_subject.replace('_', ' ')
    subject = subject.replace('_', ' ')
    TableClass = get_dynamic_table_class(table_name)
    stmt_word = select(TableClass.word).where(TableClass.group_subject == group_subject,
                                              TableClass.subject == subject)
    stmt_definition = select(TableClass.definition).where(TableClass.group_subject == group_subject, TableClass.subject == subject)
    async with AsyncSession(db.engine) as session:
        async with session.begin():
            words_result = await session.execute(stmt_word)
            definitions_result = await session.execute(stmt_definition)

            words = words_result.scalars().all()
            definitions = definitions_result.scalars().all()
            return words, definitions
