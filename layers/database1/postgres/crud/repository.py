from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from postgres.protocols.abstract_repository import IRepository
from typing import Any, Type, Callable, Coroutine
from postgres.models import DynamicTable


class CRUDPostgresRepository(IRepository[AsyncSession]):
    def __init__(self, session_factory: Callable[[], Coroutine[Any, Any, AsyncSession]]):
        self._session_factory = session_factory

    @property
    async def async_session(self) -> AsyncSession:
        return await self._session_factory()

    async def get_all(self, entity: Any):
        async with self.async_session as session:
            result = await session.execute(select(entity))
            return result.scalars().all()

    async def get_by_id(self, entity: Any, id: str):
        async with self.async_session as session:
            result = await session.execute(select(entity).where(entity.id == id))
            return result.scalar_one_or_none()

    async def add(self, entity: Any):
        async with self.async_session as session:
            session.add(entity)
            await session.commit()

    async def update(self, entity: Any):
        async with self.async_session as session:
            await session.merge(entity)
            await session.commit()

    async def delete(self, entity: Any, id: str):
        async with self.async_session as session:
            existing_entity = await self.get_by_id(entity, id)
            if existing_entity:
                await session.delete(existing_entity)
                await session.commit()

    @staticmethod
    async def create_dynamic_table(table_name: str, extend_existing: bool = True) -> Type[DynamicTable]:
        """
        Creates a table class dynamically based on the DynamicTable base model.
        """
        class Table(DynamicTable):
            __tablename__ = table_name
            __table_args__ = {'extend_existing': extend_existing}

        return Table
