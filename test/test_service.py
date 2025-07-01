from typing import List
from sxzslz.utils.logger import Logger
from sxzslz.model import User, Subset, Article
from sxzslz.service import Service
from sxzslz.service.user_service import UserService
from sxzslz.service.subset_service import SubsetService
from sxzslz.service.article_service import ArticleService

logger = Logger(__name__)


def test_user_service():
    service: Service = UserService()
    count: int = service.get_counts()
    pages: int = service.get_pages(10)
    users: List[User] = service.query_by_page(1, 10)
    logger.debug(f"User count: {count}")
    assert count > 0
    logger.debug(f"User pages: {pages}")
    assert pages > 0
    for i in users:
        logger.debug(f"User item: {i}")


def test_subset_service():
    service: Service = SubsetService()
    count: int = service.get_counts()
    pages: int = service.get_pages(10)
    users: List[Subset] = service.query_by_page(1, 10)
    logger.debug(f"Subset count: {count}")
    assert count > 0
    logger.debug(f"Subset pages: {pages}")
    assert pages > 0
    for i in users:
        logger.debug(f"Subset item: {i}")


def test_article_service():
    service: Service = ArticleService()
    count: int = service.get_counts()
    pages: int = service.get_pages(1, 10)
    users: List[Article] = service.query_by_page(1, 1, 10)
    logger.debug(f"Article count: {count}")
    assert count > 0
    logger.debug(f"Article pages: {pages}")
    assert pages > 0
    for i in users:
        logger.debug(f"Article item: {i}")
