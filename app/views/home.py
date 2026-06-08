from quart import Blueprint, render_template, g
from app.services import ArticleService


bp = Blueprint('home', __name__)

@bp.route('/')
@bp.route('/index.html')
async def index():
    crud = ArticleService(g.db_session)
    articles = await crud.get_latest_article(5)
    recommented = await crud.get_recommended_article(5)
    return await render_template('home.html', articles=articles, recommented=recommented)
