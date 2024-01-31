from sqlalchemy import create_engine, MetaData
import asyncio
from Telegram.data.database_module import engine


async def show_tables_async():
    async with engine.begin() as connection:
        metadata = MetaData()

        # Используем run_sync для выполнения инспекции
        await connection.run_sync(metadata.reflect)

        table_names = metadata.tables.keys()

        print("Таблицы в базе данных:")
        for table_name in table_names:
            print(table_name)

async def main():
    await show_tables_async()

# Запускаем цикл событий
asyncio.run(main())
