from quart import Quart, render_template
from app.views import user_bp, home_bp, news_bp


def format_datetime(value, fmt="%Y-%m-%d"):
    if not value:
        return ""
    if isinstance(value, str):
        return value
    return value.strftime(fmt)

def create_app():
    app = Quart(__name__)
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