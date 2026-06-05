from quart import Blueprint, render_template, request, redirect, url_for, session, g, flash
from sqlalchemy import select
from app.models import User


bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
async def login():
    """登录页面"""
    if request.method == 'GET':
        return await render_template('auth/login.html')

    # POST 处理登录
    form = await request.form
    username = form.get('username', '').strip()
    password = form.get('password', '').strip()

    if not username or not password:
        await flash('用户名和密码不能为空', 'error')
        return await render_template('auth/login.html')

    # 查询用户
    stmt = select(User).where(User.username == username)
    result = await g.db_session.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None or not user.check_password(password):
        await flash('用户名或密码错误', 'error')
        return await render_template('auth/login.html')

    # 登录成功，设置 session
    session['user_id'] = user.id
    session['username'] = user.username
    session['nickname'] = user.nickname

    return redirect(url_for('home.index'))


@bp.route('/logout')
async def logout():
    """退出登录"""
    session.clear()
    return redirect(url_for('home.index'))
