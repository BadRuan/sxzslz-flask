from flask import Blueprint, render_template, request, abort
from typing import List
from sxzslz.model import Subset, Article
from sxzslz.service import Service
from sxzslz.service.subset_service import SubsetService
from sxzslz.service.article_service import ArticleService


bp = Blueprint("news", __name__, url_prefix="/news")


@bp.get("/list/")
def news_list():
    subset_id: int = int(request.args.get("subset", 1))
    page: int = int(request.args.get("page", 1))
    limit: int = int(request.args.get("limit", 20))
    subset_service: Service = SubsetService()
    article_service: Service = ArticleService()
    subsets: List[Subset] = subset_service.query_by_page(1, 10)
    articles: List[Article] = article_service.query_by_page(subset_id, page, limit)
    return render_template(
        "news/list.html", subset_id=subset_id, subsets=subsets, articles=articles
    )


@bp.get("/detail/<int:article_id>/")
def news_detail(article_id: int):
    article_service: Service = ArticleService()
    article: Article | None = article_service.query_one(article_id)
    if article is None:
        abort(404)
    print(article)
    return render_template("news/detail.html", article=article)


@bp.get("/edit/")
def news_edit():
    return render_template("news/edit.html")
