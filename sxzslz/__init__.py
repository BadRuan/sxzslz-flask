from flask import Flask, redirect, url_for


def create_app():
    app = Flask(__name__)

    from sxzslz.news import bp as news

    app.register_blueprint(news)

    @app.get("/")
    def index():
        return redirect(url_for("news.news_list"))

    return app
