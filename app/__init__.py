from quart import Quart
from app.views import user_bp, home_bp


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
    
    return app

app = create_app()