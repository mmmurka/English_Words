import os
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context
from layers.database.models import Base  # Импортируйте свои модели

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение конфигурации Alembic
config = context.config

# Настройка строки подключения к базе данных из переменных окружения
config.set_main_option(
    'sqlalchemy.url',
    f'postgresql+psycopg2://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_DATABASE")}'
)

# Получение метаданных
target_metadata = Base.metadata

def run_migrations_offline():
    """
    Запуск миграций в оффлайн режиме.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Запуск миграций в онлайн режиме.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
