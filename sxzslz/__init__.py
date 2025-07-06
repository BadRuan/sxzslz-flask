from flask import Flask, redirect, url_for
from sxzslz.utils.storage import Storage


def create_app():
    app = Flask(__name__)
    app.secret_key = "1234"
    Storage.init_pool()

    from sxzslz.news import bp as news
    from sxzslz.auth import bp as auth

    app.register_blueprint(news)
    app.register_blueprint(auth)

    @app.get("/")
    def index():
        return redirect(url_for("news.news_list"))

    return app
