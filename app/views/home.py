from quart import Blueprint, render_template, g
from app.services import ArticleService


bp = Blueprint('home', __name__)

@bp.route('/')
@bp.route('/index.html')
async def index():
    service = ArticleService(g.db_session)
    articles = await service.get_latest(5)
    recommended = await service.get_recommended(5)
    return await render_template('home.html', articles=articles, recommended=recommended)
