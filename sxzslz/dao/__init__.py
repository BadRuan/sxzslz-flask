from abc import ABCMeta
from abc import abstractmethod
from typing import List, TypeVar
from sxzslz.utils.storage import Storage


T = TypeVar("T")


class Dao(metaclass=ABCMeta):

    def __init__(self, table_name: str, primary_key_name: str):
        self.table_name: str = table_name
        self.primary_key_name: str = primary_key_name

    @abstractmethod
    def add(self, *args, **kwargs) -> bool: ...

    @abstractmethod
    def update(self, *args, **kwargs) -> bool: ...

    @abstractmethod
    def query_one(self, *args, **kwargs) -> object | None: ...

    @abstractmethod
    def query_by_condition(self, *args, **kwargs) -> List: ...

    def remove(self, primary_key_id: int) -> bool:
        sql: str = f"DELETE FROM {self.table_name} WHERE {self.primary_key_name} = %s"

        with Storage() as storage:
            result = storage.remove(  # type: ignore
                sql,
                (primary_key_id,),
            )
            if result is None:
                return False
            else:
                return True

    def get_counts(self) -> int:
        sql: str = f"SELECT COUNT(*) AS count FROM {self.table_name}"
        with Storage() as storage:
            result = storage.query_one(sql, ())  # type: ignore
            if result == None:
                return 0
            return result["count"]

    def get_pages(self, page_size: int) -> int:
        sql: str = f"SELECT COUNT(*) as count FROM {self.table_name}"
        with Storage() as storage:
            total_records = storage.query_one(sql, ())  # type: ignore
            total_pages: int = (total_records["count"] + page_size - 1) // page_size  # type: ignore
            return total_pages
        return 1
