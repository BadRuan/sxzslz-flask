from abc import ABCMeta
from typing import TypeVar
from sxzslz.utils.storage import Storage
from sxzslz.utils.logger import Logger


T = TypeVar("T")
logger = Logger(__name__)


class Dao(metaclass=ABCMeta):

    def __init__(self, table_name: str, primary_key_name: str):
        self.table_name: str = table_name
        self.primary_key_name: str = primary_key_name

    def remove(self, primary_key_id: int) -> bool:
        sql: str = f"DELETE FROM {self.table_name} WHERE {self.primary_key_name} = %s"
        result = Storage.query(sql, primary_key_id)
        if result is None:
            return False
        else:
            return True

    def get_counts(self) -> int:
        sql: str = f"SELECT COUNT(*) AS count FROM {self.table_name}"
        result: int = Storage.query(sql)[0]["count"]
        return result

    def get_pages(self, page_size: int) -> int:
        sql: str = f"SELECT COUNT(*) as count FROM {self.table_name}"
        total_records: int = Storage.query(sql)[0]["count"]
        total_pages: int = (total_records + page_size - 1) // page_size
        return total_pages
