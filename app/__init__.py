from asyncio import get_event_loop
from typing import Any
from quart import Quart, render_template, g
from app.database import AsyncSessionLocal, async_engine
from app.views import user_bp, home_bp, news_bp


def format_datetime(value, fmt="%Y-%m-%d"):
    if not value:
        return ""
    if isinstance(value, str):
        return value
    return value.strftime(fmt)

async def _safe_close_session(session: Any, exception: BaseException | None) -> None:
    try:
        if exception:
            await session.rollback()
        else:
            await session.commit()
    finally:
        await session.close()

def create_app():
    app = Quart(__name__)
    
    @app.before_request
    async def before_request() -> None:
        g.db_session = AsyncSessionLocal()
    
    
    app.config["DEBUG"] = True
    app.jinja_env.filters['datetime'] = format_datetime
    
    app.register_blueprint(user_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(news_bp, url_prefix='/news')
    
    @app.errorhandler(404)
    async def handle_404(error):
        return await render_template('common/notfound.html'), 404
    
    return app

app = create_app()