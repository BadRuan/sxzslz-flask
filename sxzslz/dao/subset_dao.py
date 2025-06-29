from typing import List
from sxzslz.utils.logger import Logger
from sxzslz.utils.storage import Storage
from sxzslz.dao import Dao
from sxzslz.model import Subset


table_name: str = "subset"
primary_key_name: str = "subset_id"
logger = Logger(__name__)


class SubsetDao(Dao):

    def __init__(self):
        super().__init__(table_name, primary_key_name)

    def add(self, subset_name: str) -> bool:
        sql: str = f"""INSERT INTO {self.table_name} (subset_name) VALUES (%s);"""
        with Storage() as storage:
            storage.save(sql, (subset_name,))  # type: ignore
            return True
        return False

    def update(self, subset_id: int, subset_name: str) -> bool:
        return True

    def query_one(self, subset_id: int) -> Subset | None:
        sql: str = f"SELECT * FROM {self.table_name} WHERE {self.primary_key_name} = %s"
        with Storage() as storage:
            result = storage.query_one(sql, subset_id)  # type: ignore
            if result == None:
                return None
            else:
                return Subset(
                    subset_id=int(result["subset_id"]),
                    subset_name=result["subset_name"],
                )

    def query_by_condition(self, page: int, limit: int) -> List[Subset]:
        offset: int = (page - 1) * limit
        sql: str = f"SELECT * FROM {self.table_name} ORDER BY subset_id LIMIT %s, %s "
        with Storage() as storage:
            results = storage.query_all(sql, (offset, limit))  # type: ignore
            return [
                Subset(
                    subset_id=int(item["subset_id"]),
                    subset_name=item["subset_name"],
                )
                for item in results
            ]
