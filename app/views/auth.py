from quart import Blueprint, render_template, request, redirect, url_for, session, g, flash
from sqlalchemy import select
from app.models import User
from app.services import ArticleService, ImageService, AttachmentService
from app.crud import UserCrud


bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
async def login():
    """登录页面"""
    if request.method == 'GET':
        return await render_template('admin/login.html')

    # POST 处理登录
    form = await request.form
    username = form.get('username', '').strip()
    password = form.get('password', '').strip()

    if not username or not password:
        await flash('用户名和密码不能为空', 'error')
        return await render_template('admin/login.html')

    # 查询用户
    stmt = select(User).where(User.username == username)
    result = await g.db_session.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None or not user.check_password(password):
        await flash('用户名或密码错误', 'error')
        return await render_template('admin/login.html')

    # 登录成功，设置 session
    session['user_id'] = user.id
    session['username'] = user.username
    session['nickname'] = user.nickname

    return redirect(url_for('home.index'))

@bp.route('/dashboard')
async def dashboard():
    db_session = g.db_session
    article_service = ArticleService(db_session)
    image_service = ImageService(db_session)
    attachment_service = AttachmentService(db_session)
    user_crud = UserCrud(db_session)

    article_count = await article_service.get_counts()
    monthly_count = await article_service.get_monthly_count()
    image_count = await image_service.get_counts()
    attachment_count = await attachment_service.get_counts()
    user_count = await user_crud.get_count()
    recent_articles = await article_service.get_latest(10)

    return await render_template(
        'admin/dashboard.html',
        article_count=article_count,
        monthly_count=monthly_count,
        image_count=image_count,
        attachment_count=attachment_count,
        user_count=user_count,
        recent_articles=recent_articles
    )


@bp.route('/logout')
async def logout():
    """退出登录"""
    session.clear()
    return redirect(url_for('home.index'))
