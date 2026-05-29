from quart import Blueprint, render_template
from app.crud import get_latest_article


bp = Blueprint('home', __name__)

@bp.route('/')
async def index():
    articles = await get_latest_article(5)
    return await render_template('home.html', articles=articles)
