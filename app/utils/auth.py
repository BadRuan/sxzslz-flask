from functools import wraps
from quart import session, redirect, url_for
from app.exceptions import NotFoundError


def get_current_user_id() -> str:
    """从 session 获取当前登录用户 ID"""
    user_id = session.get('user_id')
    if not user_id:
        raise NotFoundError("用户")
    return user_id


def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return await f(*args, **kwargs)
    return decorated_function
