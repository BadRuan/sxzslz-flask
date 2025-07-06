from typing import List
from flask import Blueprint, render_template
from sxzslz.utils.logger import Logger
from sxzslz.route.station import stations
from sxzslz.model import Article
from sxzslz.service.article_service import ArticleService


bp = Blueprint("base", __name__)
logger = Logger(__name__)


@bp.get("/")
def index():
    article_service: ArticleService = ArticleService()
    news_articles: List[Article] = article_service.query_by_page(1, 1, 10)
    notice_articles: List[Article] = article_service.query_by_page(2, 1, 10)
    file_articles: List[Article] = article_service.query_by_page(3, 1, 8)
    return render_template(
        "home.html",
        news=news_articles,
        notice=notice_articles,
        file=file_articles,
        stations=stations,
    )
