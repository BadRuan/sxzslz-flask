from quart import Blueprint, render_template, request, g
from app.services import ArticleService, CategoryService


bp = Blueprint('article', __name__)

@bp.route('/list/index.html')
@bp.route('/list/<int:category_id>.html')
async def list(category_id: int = 1):
    session = g.db_session
    category_service = CategoryService(session)
    article_service = ArticleService(session)

    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    categories = await category_service.get_all_categories()
    news_list, total = await article_service.get_articles_paginated(
        page=page,
        per_page=per_page,
        category_id=category_id
    )

    # 计算分页信息
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1

    return await render_template(
        'news/list.html',
        categories=categories,
        news_list=news_list,
        category_id=category_id,
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages
    )

@bp.route('/<article_slug>.html')
async def detail(article_slug: str):
    service = ArticleService(g.db_session)
    detail = await service.get_article_detail(article_slug)
    if detail is None:
        return await render_template('common/notfound.html'), 404
    else:
        return await render_template('news/detail.html', news=detail)
