from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, TypeVar, Generic

TSession = TypeVar('TSession', bound=AsyncSession)


class IAsyncSessionFactory(ABC, Generic[TSession]):
    @abstractmethod
    async def __call__(self, *args: Any, **kwds: Any) -> AsyncSession:
        raise NotImplementedError
