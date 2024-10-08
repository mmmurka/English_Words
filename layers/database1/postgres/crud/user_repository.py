from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
import logging
from layers.database.models import User
from postgres.crud.repository import CRUDPostgresRepository

from postgres.sql.repository import SessionFactory

logging.basicConfig(level=logging.INFO)


class PostgresUserRepository(CRUDPostgresRepository):
    def __init__(self, session_factory: SessionFactory):
        super().__init__(session_factory)

    async def create_user(self, tg_user_id: int, name: str, username: str):
        async with await self._session_factory() as session:
            try:
                # Search for an existing user
                stmt = select(User).filter(User.id == tg_user_id)
                result = await session.execute(stmt)
                existing_user = result.scalar()

                if existing_user:
                    logging.info(f"User {name} already exists in the database.")
                    return existing_user
                else:
                    # Adding a new user
                    user = User(id=tg_user_id, name=name, username=username)
                    session.add(user)
                    await session.commit()
                    logging.info(f"User {name} with ID {tg_user_id} added to the database.")
                    return user
            except SQLAlchemyError as e:
                await session.rollback()
                logging.error(f"Error occurred: {e}")
                raise
