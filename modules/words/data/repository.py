from asyncio import Lock
from typing import Type

from layers.database.models import DynamicTable
from postgres.crud.repository import ReadRepository

_dynamic_class_cache = {}
_cache_lock = Lock()


class WordRepository(ReadRepository):

    async def get_dynamic_table_class(self, table_name: str) -> Type[DynamicTable]:
        """
        Асинхронно возвращает класс таблицы на основе DynamicTable.
        Если класс не был создан ранее, он создается и сохраняется в кэше.
        """
        async with _cache_lock:
            if table_name not in _dynamic_class_cache:
                # Динамически создаем класс таблицы
                class TableClass(DynamicTable):
                    __tablename__ = table_name
                    __table_args__ = {'extend_existing': True}

                _dynamic_class_cache[table_name] = TableClass
            return _dynamic_class_cache[table_name]

    async def querry_accepter(self, query):
        async with (await self.async_session) as session:
            result = await session.execute(query)
            result = result.scalars().all()
            return result

    async def get_group_subjects(self, table_name: str):

        TableClass = await self.get_dynamic_table_class(table_name)
        query = self._queryWithParams(TableClass.group_subject.distinct())
        return sorted(await self.querry_accepter(query))

    async def get_subjects(self, table_name: str, group_subject: str):

        TableClass = await self.get_dynamic_table_class(table_name)
        query = self._queryWithParams(TableClass.subject.distinct(), filters=[TableClass.group_subject == group_subject])
        return sorted(await self.querry_accepter(query), key=lambda x: int(x.split('-')[0].strip()))


    async def get_words(self, table_name: str, group_subject: str, subject: str):

        TableClass = await self.get_dynamic_table_class(table_name)
        word_query = self._queryWithParams(TableClass.word, filters=[TableClass.group_subject == group_subject,
                                      TableClass.subject == subject])
        definition_query = self._queryWithParams(TableClass.definition, filters=[TableClass.group_subject == group_subject,
                                      TableClass.subject == subject])


        return await self.querry_accepter(word_query), await self.querry_accepter(definition_query)
