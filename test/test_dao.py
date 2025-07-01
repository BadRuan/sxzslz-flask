from typing import List
from sxzslz.utils.logger import Logger
from sxzslz.model import User, Subset, Article
from sxzslz.dao import Dao

from sxzslz.dao.user_dao import UserDao
from sxzslz.dao.subset_dao import SubsetDao
from sxzslz.dao.article_dao import ArticleDao

logger = Logger(__name__)


def test_user_dao():
    dao: Dao = UserDao()
    count: int = dao.get_counts()
    assert count > 0
    pages: int = dao.get_pages(10)
    assert pages > 0

    user: User | None = dao.query_one(1000)
    assert None == user

    users: List[User] = dao.query_by_condition(1, 10)
    assert len(users) > 0


# def test_add_user():
#     dao: Dao = UserDao()
#     user_name, nick_name, password, avatar_src = "ruan", "ruan", "123456", "1234"
#     affected_rows = dao.add(user_name, nick_name, password, avatar_src)
#     logger.debug(f"Affected_rows => {affected_rows}")


def test_subset_dao():
    dao: Dao = SubsetDao()

    count: int = dao.get_counts()
    assert count > 0

    pages: int = dao.get_pages(10)
    assert pages > 0

    subset: Subset | None = dao.query_one(1000)
    assert None == subset

    users: List[Subset] = dao.query_by_condition(1, 10)
    assert len(users) > 0


def test_article_dao():
    dao: Dao = ArticleDao()

    count: int = dao.get_counts()
    assert count > 0

    pages: int = dao.get_pages(1, 10)
    assert pages > 0

    article: Article | None = dao.query_one(10100)
    assert None == article

    users: List[Article] = dao.query_by_condition(1, 1, 10)
    assert len(users) > 0
