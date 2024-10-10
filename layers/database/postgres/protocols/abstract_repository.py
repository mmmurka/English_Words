from __future__ import annotations
from postgres.protocols.async_session import TSession
from abc import ABC, abstractmethod
from typing import Generic


class IRepository(ABC, Generic[TSession]):
    @abstractmethod
    def __init__(self, async_session: TSession) -> None:
        raise NotImplemented

    @property
    @abstractmethod
    async def async_session(self) -> TSession:
        raise NotImplemented
