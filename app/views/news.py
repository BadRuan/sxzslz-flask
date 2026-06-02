from quart import Blueprint, render_template, g
from app.crud import CategoryCrud, ArticleCrud


bp = Blueprint('news', __name__)

@bp.route('/list/')
@bp.route('/list/<int:category_id>')
async def list(category_id: int = 1):
    session = g.db_session
    category_crud = CategoryCrud(session)
    article_crud = ArticleCrud(session)
    categories = await category_crud.get_public_categories()
    news_list = await article_crud.get_latest_article(5)
    return await render_template('news/list.html', categories=categories, news_list=news_list, category_id=category_id)

@bp.route('/detail/<int:article_id>')
async def detail(article_id: int):
    crud = ArticleCrud(g.db_session)
    detail = await crud.get_article_detail(article_id)
    if detail is None:
        return await render_template('common/notfound.html'), 404
    else:
        return await render_template('news/detail.html', news=detail)
