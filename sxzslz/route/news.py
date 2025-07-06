from typing import List
from flask import Blueprint, render_template, request, abort, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField
from wtforms.validators import DataRequired, Length
from sxzslz.model import User, Subset, Article
from sxzslz.utils.logger import Logger
from sxzslz.utils.pagination import Paginator
from sxzslz.service.user_service import UserService
from sxzslz.service.subset_service import SubsetService
from sxzslz.service.article_service import ArticleService


bp = Blueprint("news", __name__, url_prefix="/news")
logger = Logger(__name__)


@bp.get("/list/")
def news_list():
    subset_id: int = int(request.args.get("subset", 1))
    page: int = int(request.args.get("page", 1))
    limit: int = int(request.args.get("limit", 20))
    subset_service: SubsetService = SubsetService()
    article_service: ArticleService = ArticleService()
    subsets: List[Subset] = subset_service.query_by_page(1, 10)
    articles: List[Article] = article_service.query_by_page(subset_id, page, limit)
    total = article_service.get_counts(subset_id)
    paginator: Paginator = Paginator(
        total=total,
        page=page,
        subset_id=subset_id,
        per_page=limit,
        endpoint="news.news_list",
    )
    return render_template(
        "news/list.html",
        paginator=paginator,
        subset_id=subset_id,
        subsets=subsets,
        articles=articles,
    )


@bp.get("/detail/<int:article_id>/")
def news_detail(article_id: int):
    article_service: ArticleService = ArticleService()
    article: Article | None = article_service.query_one(article_id)
    if article is None:
        abort(404)
    else:
        user_service: UserService = UserService()
        user: User | None = user_service.query_one(article.user_id)
    return render_template("news/detail.html", article=article, user=user)


class ArticleForm(FlaskForm):
    # 获取文章类别
    subset_service: SubsetService = SubsetService()
    subsets = subset_service.query_by_page(1, 10)
    subsets = tuple([(subset.subset_id, subset.subset_name) for subset in subsets])

    title = StringField(
        "文章标题: ",
        validators=[
            DataRequired(),
            Length(5, 48),
        ],
    )
    subset_id = RadioField(
        "文章类别: ",
        validators=[
            DataRequired(),
        ],
        choices=(subsets),
    )
    content = StringField(render_kw={"id": "content", "type": "hidden"})
    submit = SubmitField("点击立即发布")


@bp.route("/edit/", methods=["GET", "POST"])
def news_edit():
    form = ArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        subset_id = form.subset_id.data
        content = form.content.data
        article_service: ArticleService = ArticleService()
        article_service.add(int(subset_id), 1, title=title, content=content)  # type: ignore
        return redirect(url_for("news.news_list"))
    return render_template("news/editor.html", form=form)
