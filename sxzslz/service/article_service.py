from typing import List
from sxzslz.utils.logger import Logger
from sxzslz.model import Article
from sxzslz.dao.article_dao import ArticleDao
from sxzslz.dao.subset_dao import SubsetDao


logger = Logger(__name__)


def check_num(num: int, default: int = 1) -> int:
    if num <= 0:
        return default
    else:
        return num


class ArticleService:

    def __init__(self):
        self._dao: ArticleDao = ArticleDao()

    def get_counts(self, subset_id: int) -> int:
        return self._dao.get_counts(subset_id)

    def add(self, subset_id: int, user_id: int, title: str, content: str) -> bool:
        subset_id = check_num(subset_id)
        return self._dao.add(subset_id, user_id, title, content)

    def query_by_page(self, subset_id: int, page: int, limit: int) -> List[Article]:
        subset_id = check_num(subset_id, 1)
        page = check_num(page, 1)
        limit = check_num(limit, 15)
        subsetDao: SubsetDao = SubsetDao()
        counts: int = subsetDao.get_counts()
        if subset_id > counts:
            subset_id = 1

        return self._dao.query_by_condition(subset_id, page, limit)

    def query_one(self, id: int) -> Article | None:
        if id <= 0:
            return None
        article: Article | None = self._dao.query_one(id)
        if article is None:
            return None
        else:
            # 获取文章详情时增加1次阅读量
            self._dao.add_read_count(id)
            return article
