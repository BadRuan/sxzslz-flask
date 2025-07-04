from flask import Flask, redirect, url_for
from sxzslz.utils.storage import Storage


def create_app():
    app = Flask(__name__)
    Storage.init_pool()

    from sxzslz.news import bp as news

    app.register_blueprint(news)

    @app.get("/")
    def index():
        return redirect(url_for("news.news_list"))

    return app
