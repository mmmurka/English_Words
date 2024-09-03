import pytest
from alembic import command
from alembic.config import Config
import os


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    os.environ['DB_URL'] = 'postgresql+psycopg2://mmmurka:12341@localhost/englishwords_test'

    # Создаем конфигурацию Alembic
    alembic_cfg = Config("alembic.ini")

    # Выполняем миграции
    command.upgrade(alembic_cfg, "head")

    yield

    # Дополнительно можно добавить код для очистки тестовой БД после тестов


