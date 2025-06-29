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
    pages: int = dao.get_pages(10)
    users: List[User] = dao.query_by_condition(1, 10)
    logger.debug(f"User count: {count}")
    assert count > 0
    logger.debug(f"User pages: {pages}")
    assert pages > 0
    for i in users:
        logger.debug(f"User item: {i}")


def test_subset_dao():
    dao: Dao = SubsetDao()
    count: int = dao.get_counts()
    pages: int = dao.get_pages(10)
    users: List[Subset] = dao.query_by_condition(1, 10)
    logger.debug(f"Subset count: {count}")
    assert count > 0
    logger.debug(f"Subset pages: {pages}")
    assert pages > 0
    for i in users:
        logger.debug(f"Subset item: {i}")


def test_article_dao():
    dao: Dao = ArticleDao()
    count: int = dao.get_counts()
    pages: int = dao.get_pages(10)
    users: List[Article] = dao.query_by_condition(1, 1, 10)
    logger.debug(f"Article count: {count}")
    assert count > 0
    logger.debug(f"Article pages: {pages}")
    assert pages > 0
    for i in users:
        logger.debug(f"Article item: {i}")
