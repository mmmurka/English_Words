from logging import critical
from typing import Type


from postgres.base_repository import ReadRepository
from postgres.models import DynamicTable


class CRUDPostgresRepository(ReadRepository):

    @staticmethod
    async def create_dynamic_table(table_name: str, extend_existing: bool = True) -> Type[DynamicTable]:
        """
        Creates a table class dynamically based on the DynamicTable base model.
        """

        class Table(DynamicTable):
            __tablename__ = table_name
            __table_args__ = {'extend_existing': extend_existing}

        return Table
