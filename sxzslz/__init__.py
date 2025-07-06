from flask import Flask
from sxzslz.utils.storage import Storage


def create_app():
    app = Flask(__name__)
    app.secret_key = "1234"
    Storage.init_pool()

    from sxzslz.route.base import bp as base
    from sxzslz.route.news import bp as news
    from sxzslz.route.auth import bp as auth
    from sxzslz.route.station import bp as station

    app.register_blueprint(base)
    app.register_blueprint(news)
    app.register_blueprint(auth)
    app.register_blueprint(station)

    return app
