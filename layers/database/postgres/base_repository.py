from logging import critical
from tkinter.tix import Select
from typing import Any, Optional, Callable, Sequence

from sqlalchemy import select

from postgres.sql.repository import SqlAlchemyRepository


class Repository(SqlAlchemyRepository):
    async def saveChanges(self):
        async with (await self.async_session) as session:
            try:
                await session.commit()
            except Exception as err:
                critical(err)
                await session.rollback()
                raise err

    @staticmethod
    def buildQuery(*entities: Any) -> Select:
        return select(*entities)

    async def fetch(self, *entities: Any, modifier: Optional[Callable[[Any], Any]] = None) -> Sequence[Any]:
        query = self.buildQuery(*entities)
        if modifier is not None:
            query = modifier(query)

        async with (await self.async_session) as session:
            result = await session.execute(query)
            return result.unique().all()

    async def fetchColumn(self, column: Any, *filters: Any) -> Sequence[Any]:
        query = self.buildQuery(column)
        query = query.filter(*filters).distinct()

        async with (await self.async_session) as session:
            result = await session.scalars(query)
            return result.unique().all()


class ReadRepository(Repository):

    @staticmethod
    def _query(*entities: Any) -> Select:
        return select(*entities)

    @staticmethod
    def _queryWithParams(*columns: Any, filters: Optional[Any] = None, group: Optional[Any] = None) -> Select:
        """
        Строит SQL-запрос с указанными колонками, фильтрами и опциональной группировкой.
        :param columns: Колонки, которые нужно выбрать
        :param filters: Фильтры для SQL-запроса
        :param group: Колонка для группировки (если нужно)
        :return: Объект SQL-запроса Select
        """
        query = select(*columns)

        if group is not None:
            query = query.group_by(group)

        if filters:
            query = query.filter(*filters)

        return query
