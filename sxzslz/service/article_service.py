from typing import List
from sxzslz.utils.logger import Logger
from sxzslz.model import Article
from sxzslz.dao import Dao
from sxzslz.dao.article_dao import ArticleDao
from sxzslz.dao.subset_dao import SubsetDao
from sxzslz.service import Service


logger = Logger(__name__)


def check_num(num: int, default: int = 1) -> int:
    if num <= 0:
        return default
    else:
        return num


class ArticleService(Service):

    def __init__(self):
        super().__init__()
        self._dao: Dao = ArticleDao()

    def add(
        self,
        subset_id: int,
        user_id: int,
        title: str,
        content: str,
        img_src: str,
        state: bool,
    ) -> bool:
        return self._dao.add(subset_id, user_id, title, content, img_src, state)

    def query_by_page(self, subset_id: int, page: int, limit: int) -> List[Article]:  # type: ignore
        subset_id = check_num(subset_id, 1)
        page = check_num(page, 1)
        limit = check_num(limit, 15)
        subsetDao: Dao = SubsetDao()
        counts: int = subsetDao.get_counts(subset_id)
        if subset_id > counts:
            subset_id = 1

        return self._dao.query_by_condition(subset_id, page, limit)

    def query_one(self, id: int) -> Article | None:
        self._dao.add_read_count(id)  # type: ignore
        return self.query_one(id)
