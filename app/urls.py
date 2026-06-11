from quart import Blueprint
from app.modules.home.views import bp as home_bp
from app.modules.home.views_auth import bp as auth_bp
from app.modules.home.views_article import bp as article_bp
from app.modules.admin.views import bp as admin_bp
from app.modules.image.views import bp as image_bp
from app.modules.attachment.views import bp as attachment_bp

urlpatterns: list[tuple[Blueprint, str]] = [
    (home_bp, ''),
    (auth_bp, ''),
    (article_bp, '/article'),
    (image_bp, '/image'),
    (attachment_bp, '/attachment'),
    (admin_bp, '/admin'),
]
