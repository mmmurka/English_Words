from layers.database.models import DynamicTable


def create_table_class(tablename, extend_existing=True):
    """Создает класс таблицы динамически на основе базовой модели."""
    class Table(DynamicTable):
        __tablename__ = tablename
        __table_args__ = {'extend_existing': extend_existing}

    return Table
