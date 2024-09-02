from sqlalchemy.ext.asyncio import AsyncSession
from layers.database.controller.database_module import engine
from layers.database.models import User
from sqlalchemy.future import select
import layers.database.models as db_models
import logging

logging.basicConfig(level=logging.INFO)


async def create_user(tg_user_id: int, name: str, username: str):
    async with AsyncSession(engine) as session:
        try:
            stmt = select(db_models.User).filter(db_models.User.id == tg_user_id)
            result = await session.execute(stmt)
            existing_user = result.scalar()

            if existing_user:
                logging.info(f'User {name} already exists in the database.')
                # Завершаем сессию через rollback, так как изменений не было
                await session.rollback()
            else:
                user = User(id=tg_user_id, name=name, username=username)
                session.add(user)
                await session.commit()
                logging.info(f'User {name} with ID {tg_user_id} added to the database.')
        except Exception as e:
            # Если возникла ошибка, откатываем транзакцию
            await session.rollback()
            logging.error(f'Error occurred: {e}')
            raise
