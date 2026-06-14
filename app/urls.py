from quart import Blueprint
from app.views.article_views import bp as article_bp

urlpatterns: list[tuple[Blueprint, str]] = [
    (article_bp, '/article'),
]
