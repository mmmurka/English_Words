from typing import Callable, Coroutine, Any

from sqlalchemy.ext.asyncio import AsyncSession

from postgres.protocols.abstract_repository import IRepository

SessionFactory = Callable[[], Coroutine[Any, Any, AsyncSession]] #   session_factory - це callable, який повертає сесію

class SqlAlchemyRepository(IRepository[AsyncSession]):
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    @property
    async def async_session(self) -> AsyncSession:
        return await self._session_factory()
