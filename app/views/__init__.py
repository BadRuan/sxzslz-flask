from .user import bp as user_bp
from .home import bp as home_bp
from .article import bp as article_bp
from .image import bp as image_bp
from .auth import bp as auth_bp
from .attachment import bp as attachment_bp
from .admin import bp as admin_bp


__all__ = [
    'user_bp',
    'home_bp',
    'article_bp',
    'image_bp',
    'auth_bp',
    'attachment_bp',
    'admin_bp'
]