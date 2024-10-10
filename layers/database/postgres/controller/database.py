from __future__ import annotations

import os

from postgres.protocols.async_session import IAsyncSessionFactory
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import Any, Optional
from dotenv import load_dotenv

load_dotenv()


class DBConfig:
    def __init__(self, engine: str, host: str, port: str, username: str, password: str, dbName: str, **kwargs):
        self.__engine = engine
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__dbName = dbName

    @property
    def protocol(self) -> str:
        if self.__engine == "postgres":
            return "postgresql+asyncpg"
        raise NotImplementedError("Proto not supported")

    def buildConnectionAddress(self, dbName: Optional[str] = None) -> str:
        dbName = self.__dbName if dbName is None else dbName
        return f'{self.protocol}://{self.__username}:{self.__password}@{self.__host}:{self.__port}/{dbName}'

    @staticmethod
    def getLocalConfig() -> DBConfig:
        return DBConfig(
            engine=os.getenv("DB_ENGINE", "postgres"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", 5432),
            username=os.getenv("DB_USER"),
            password=os.getenv('DB_PASSWORD'),
            dbName=os.getenv("DB_DATABASE"),
        )
        # TODO настроить конфигурацию к бд-шке, проблема с тем что ретернит дбконфиг


class DBManager(IAsyncSessionFactory[AsyncSession]):
    def __init__(self, config: Optional[dict] = None):
        self.__config = DBConfig(**config) if config else DBConfig.getLocalConfig()
        self.__engine = create_async_engine(self.__config.buildConnectionAddress(os.getenv("DB_DATABASE")))
        self.__sessionFactory = async_sessionmaker(bind=self.__engine, expire_on_commit=False)

    async def __call__(self, *args: Any, **kwds: Any) -> AsyncSession:
        return self.__sessionFactory()

    async def close(self):
        if self.__engine:
            await self.__engine.dispose()

    async def getSession(self) -> AsyncSession:
        return self.__sessionFactory()
