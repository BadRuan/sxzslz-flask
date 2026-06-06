from .user import bp as user_bp
from .home import bp as home_bp
from .news import bp as news_bp
from .image import bp as image_bp
from .auth import bp as auth_bp
from .attachment import bp as attachment_bp


__all__ = [
    'user_bp',
    'home_bp',
    'news_bp',
    'image_bp',
    'auth_bp',
    'attachment_bp'
]