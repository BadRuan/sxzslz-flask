from os import makedirs
from quart import Quart, render_template, g
from app.settings import settings, Upload_Config
from app.database import AsyncSessionLocal
from app.views import user_bp, home_bp, news_bp, image_bp, auth_bp


def format_datetime(value, fmt="%Y-%m-%d"):
    if not value:
        return ""
    if isinstance(value, str):
        return value
    return value.strftime(fmt)

def create_app():
    app = Quart(__name__)


    @app.before_request
    async def before_request() -> None:
        g.db_session = AsyncSessionLocal()


    @app.teardown_request
    async def teardown_request(exception):
        session = g.pop('db_session', None)
        if session is not None:
            try:
                if exception:
                    await session.rollback()
                else:
                    await session.commit()
            finally:
                await session.close()


    app.config["DEBUG"] = settings.DEBUG
    app.config["MAX_CONTENT_LENGTH"] = Upload_Config.MAX_CONTENT_LENGTH
    app.secret_key = settings.SECRET_KEY
    app.jinja_env.filters['datetime'] = format_datetime

    makedirs(Upload_Config.UPLOAD_FOLDER, exist_ok=True)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(news_bp, url_prefix='/news')
    app.register_blueprint(image_bp, url_prefix='/image')

    @app.errorhandler(404)
    async def handle_404(error):
        return await render_template('common/notfound.html'), 404

    return app

app = create_app()