import os
from sqlalchemy import engine_from_config, pool
from alembic import context
from layers.database.models import Base


config = context.config
db_url = os.getenv('DB_URL')

if db_url:
    config.set_main_option('sqlalchemy.url', db_url)

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
