from asyncio import Lock
from typing import Type

from sqlalchemy.exc import SQLAlchemyError

from layers.database.postgres.models import DynamicTable
from postgres.crud.repository import ReadRepository

_dynamic_class_cache = {}
_cache_lock = Lock()


class WordRepository(ReadRepository):

    @staticmethod
    async def get_dynamic_table_class(table_name: str) -> Type[DynamicTable]:
        """
        Асинхронно возвращает класс таблицы на основе DynamicTable.
        Если класс не был создан ранее, он создается и сохраняется в кэше.
        """
        async with _cache_lock:
            if table_name not in _dynamic_class_cache:
                class TableClass(DynamicTable):
                    __tablename__ = table_name
                    __table_args__ = {'extend_existing': True}

                _dynamic_class_cache[table_name] = TableClass
            return _dynamic_class_cache[table_name]

    async def execute_query(self, query):  # Выполняет асинхронный запрос к базе данных и возвращает результат
        try:
            async with (await self.async_session) as session:
                result = await session.execute(query)
                return result.scalars().all()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Ошибка выполнения запроса: {e}") from e

    def build_query(self, column, filters=None):  # Вспомогательный метод для построения запросов с учетом фильтров
        query = self._queryWithParams(column, filters=filters or [])
        return query

    @staticmethod
    def build_filters(table_class, group_subject=None, subject=None):  # Вспомогательный метод для создания фильтров
        filters = []
        if group_subject:
            filters.append(table_class.group_subject == group_subject)
        if subject:
            filters.append(table_class.subject == subject)
        return filters

    async def get_distinct_group_subjects(self, table_name: str):  # Возвращает список уникальных group_subject из таблицы
        TableClass = await self.get_dynamic_table_class(table_name)
        query = self.build_query(TableClass.group_subject.distinct())
        result = await self.execute_query(query)  # Выполняем запрос
        return sorted(result)

    async def get_distinct_subjects(self, table_name: str, group_subject: str):  # Возвращает список уникальных subjects для указанного group_subject
        TableClass = await self.get_dynamic_table_class(table_name)
        filters = self.build_filters(TableClass, group_subject=group_subject)
        query = self.build_query(TableClass.subject.distinct(), filters=filters)
        result = await self.execute_query(query)  # Выполняем запрос
        # Сортировка subjects по числовому значению перед дефисом
        return sorted(result, key=lambda x: int(x.split('-')[0].strip()))

    async def get_words_and_definitions(self, table_name: str, group_subject: str, subject: str):  # Возвращает слова и их определения для указанного group_subject и subject
        TableClass = await self.get_dynamic_table_class(table_name)
        filters = self.build_filters(TableClass, group_subject=group_subject, subject=subject)

        word_query = self.build_query(
            TableClass.word,
            filters=filters
        )

        definition_query = self.build_query(
            TableClass.definition,
            filters=filters
        )

        words = await self.execute_query(word_query)
        definitions = await self.execute_query(definition_query)

        return words, definitions
