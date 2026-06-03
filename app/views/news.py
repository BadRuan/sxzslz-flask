from quart import Blueprint, render_template, request, g
from app.crud import CategoryCrud, ArticleCrud


bp = Blueprint('news', __name__)

@bp.route('/list/')
@bp.route('/list/<int:category_id>')
async def list(category_id: int = 1):
    session = g.db_session
    category_crud = CategoryCrud(session)
    article_crud = ArticleCrud(session)

    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # 限制每页数量
    per_page = min(per_page, 50)

    categories = await category_crud.get_public_categories()
    news_list, total = await article_crud.get_articles_paginated(
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

@bp.route('/detail/<int:article_id>')
async def detail(article_id: int):
    crud = ArticleCrud(g.db_session)
    detail = await crud.get_article_detail(article_id)
    if detail is None:
        return await render_template('common/notfound.html'), 404
    else:
        return await render_template('news/detail.html', news=detail)
