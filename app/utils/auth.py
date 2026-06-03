from hashlib import sha256
from functools import wraps
from quart import session, redirect, url_for


def hash_password(password: str) -> str:
    """对密码进行 SHA256 哈希"""
    return sha256(password.encode('utf-8')).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """验证密码是否匹配"""
    return hash_password(password) == password_hash


def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return await f(*args, **kwargs)
    return decorated_function
