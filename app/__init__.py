from quart import Quart
from app.views import user_bp, home_bp


def create_app():
    app = Quart(__name__)
    app.config["DEBUG"] = True 

    app.register_blueprint(user_bp)
    app.register_blueprint(home_bp)
    
    return app

app = create_app()