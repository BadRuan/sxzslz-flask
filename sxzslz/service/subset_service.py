from typing import List
from sxzslz.model import Subset
from sxzslz.dao.subset_dao import SubsetDao


class SubsetService:

    def __init__(self):
        self._dao: SubsetDao = SubsetDao()

    def add(
        self,
        subset_name: str,
    ) -> bool:
        return self._dao.add(subset_name)

    def query_by_page(self, page: int, limit: int) -> List[Subset]:
        return self._dao.query_by_condition(page, limit)
