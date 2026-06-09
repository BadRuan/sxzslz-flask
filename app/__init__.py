from os import makedirs
from quart import Quart, render_template, g
from app.settings import settings
from app.database import AsyncSessionLocal, async_engine
from app.views import user_bp, home_bp, article_bp, image_bp, auth_bp, attachment_bp, admin_bp


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


    @app.after_serving
    async def shutdown_engine():
        await async_engine.dispose()


    app.config["DEBUG"] = settings.DEBUG
    app.config["MAX_CONTENT_LENGTH"] = settings.MAX_CONTENT_LENGTH
    app.secret_key = settings.SECRET_KEY
    app.jinja_env.filters['datetime'] = format_datetime

    makedirs(settings.IMAGE_UPLOAD_FOLDER, exist_ok=True)
    makedirs(settings.ATTACHMENT_UPLOAD_FOLDER, exist_ok=True)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(article_bp, url_prefix='/article')
    app.register_blueprint(image_bp, url_prefix='/image')
    app.register_blueprint(attachment_bp, url_prefix='/attachment')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @app.errorhandler(404)
    async def handle_404(error):
        return await render_template('common/notfound.html'), 404

    return app

app = create_app()