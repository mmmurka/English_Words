import sqlalchemy.orm
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os


load_dotenv()

db_config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_DATABASE"),
}

DATABASE_URL = f"postgresql+asyncpg://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

engine = create_async_engine(DATABASE_URL, echo=True)

Base = sqlalchemy.orm.declarative_base()
