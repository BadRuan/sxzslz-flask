from sxzslz.dao import Dao
from sxzslz.dao.subset_dao import SubsetDao
from sxzslz.service import Service


class SubsetService(Service):

    def __init__(self):
        super().__init__()
        self._dao: Dao = SubsetDao()

    def add(
        self,
        subset_name: str,
    ) -> bool:
        return self._dao.add(subset_name)

    def update(self, subset_id: int, subset_name: str) -> bool:
        if subset_id <= 0:
            return False
        else:
            count: int = self.get_counts(0)
            if subset_id > count:
                return False
        return self._dao.update(subset_id, subset_name)
