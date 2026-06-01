from quart import Blueprint, render_template
from app.crud import get_latest_article, get_public_categories, get_article_detail


bp = Blueprint('news', __name__)

@bp.route('/list/')
@bp.route('/list/<int:category_id>')
async def list(category_id: int = 1):
    categories = await get_public_categories()
    news_list = await get_latest_article(5)
    return await render_template('news/list.html', categories=categories, news_list=news_list, category_id=category_id)

@bp.route('/detail/<int:article_id>')
async def detail(article_id: int):
    detail = await get_article_detail(article_id)
    if detail is None:
        return await render_template('common/notfound.html'), 404
    else:
        return await render_template('news/detail.html', news=detail)
