from functools import wraps
from quart import session, redirect, url_for


def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return await f(*args, **kwargs)
    return decorated_function
