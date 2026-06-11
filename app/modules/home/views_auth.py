from quart import Blueprint, render_template, request, redirect, url_for, session, g, flash
from app.modules.admin.services import UserService


bp = Blueprint('auth', __name__)
path_prefix: str = 'admin/'

@bp.route('/login', methods=['GET', 'POST'])
async def login():
    """登录页面"""
    full_path: str = path_prefix + 'login.html'
    if request.method == 'GET':
        return await render_template(full_path)

    # POST 处理登录
    form = await request.form
    username = form.get('username', '').strip()
    password = form.get('password', '').strip()

    if not username or not password:
        await flash('用户名和密码不能为空', 'error')
        return await render_template(full_path)

    # 通过 service 查询用户
    user_service = UserService(g.db_session)
    user = await user_service.get_by_username(username)

    if user is None or not user.check_password(password):
        await flash('用户名或密码错误', 'error')
        return await render_template(full_path)

    # 登录成功，设置 session
    session['user_id'] = user.id
    session['username'] = user.username
    session['nickname'] = user.nickname

    return redirect(url_for('admin.dashboard'))


@bp.route('/logout')
async def logout():
    """退出登录"""
    session.clear()
    return redirect(url_for('home.index'))
