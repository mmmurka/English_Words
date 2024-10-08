from logging import critical
from typing import Type, Any, Optional, Callable, Sequence

from sqlalchemy import Select

from postgres.models import DynamicTable
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

    def buildQuery(self, *entities: Any) -> Select:
        return Select(*entities)

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

    def _query(self, *entities: Any) -> Select:
        return Select(*entities)

    def _queryWithParams(self, *filters: Any, group: Optional[Any] = None) -> Select:
        query = self._query()

        if group is not None:
            query = query.group_by(group)

        if filters:
            query = query.filter(*filters)

        return query


class CRUDPostgresRepository(ReadRepository):

    @staticmethod
    async def create_dynamic_table(table_name: str, extend_existing: bool = True) -> Type[DynamicTable]:
        """
        Creates a table class dynamically based on the DynamicTable base model.
        """

        class Table(DynamicTable):
            __tablename__ = table_name
            __table_args__ = {'extend_existing': extend_existing}

        return Table
