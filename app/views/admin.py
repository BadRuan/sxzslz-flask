from quart import Blueprint, render_template, request, g, redirect, url_for, flash
from app.services import ArticleService, CategoryService, ImageService
from app.utils import login_required, get_current_user_id


bp = Blueprint('admin', __name__)

@bp.route('/list')
@login_required
async def article_list():
    """后台文章列表"""
    db_session = g.db_session
    article_service = ArticleService(db_session)
    category_service = CategoryService(db_session)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)

    articles, total = await article_service.get_admin_paginated(
        page=page, per_page=per_page
    )
    categories = await category_service.get_all()
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1

    return await render_template(
        'admin/article_list.html',
        articles=articles,
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages
    )


@bp.route('/create', methods=['GET'])
@login_required
async def create_form():
    """文章创建表单"""
    db_session = g.db_session
    category_service = CategoryService(db_session)
    categories = await category_service.get_all()
    return await render_template('admin/article_edit.html', categories=categories)


@bp.route('/create', methods=['POST'])
@login_required
async def handle_create():
    """处理文章创建"""
    form_data = await request.form
    files = await request.files

    title = form_data.get('title', '').strip()
    category_id = form_data.get('category_id', type=int)
    content = form_data.get('content', '').strip()
    is_public = form_data.get('is_public') == 'on'

    # 参数校验
    if not title:
        await flash('文章标题不能为空', 'error')
        return redirect(url_for('admin.create_form'))
    if not category_id:
        await flash('请选择分类', 'error')
        return redirect(url_for('admin.create_form'))
    if not content:
        await flash('文章内容不能为空', 'error')
        return redirect(url_for('admin.create_form'))

    db_session = g.db_session
    user_id = get_current_user_id()
    image_id = None

    # 处理可选的封面图片
    if 'cover_image' in files and files['cover_image'].filename:
        image = await ImageService(db_session).upload(files['cover_image'], user_id)
        image_id = image.id

    # 创建文章
    article_service = ArticleService(db_session)
    await article_service.create(
        category_id=category_id,
        user_id=user_id,
        title=title,
        image_id=image_id,
        content=content,
        is_public=is_public
    )

    await flash('文章创建成功', 'success')
    return redirect(url_for('admin.article_list'))


@bp.route('/article/<int:article_id>/edit', methods=['GET'])
@login_required
async def edit_form(article_id: int):
    """文章编辑表单"""
    db_session = g.db_session
    article_service = ArticleService(db_session)
    category_service = CategoryService(db_session)

    article = await article_service.get_by_id(article_id)
    if article is None:
        await flash('文章不存在', 'error')
        return redirect(url_for('admin.article_list'))

    categories = await category_service.get_all()
    return await render_template('admin/article_edit.html', article=article, categories=categories)


@bp.route('/article/<int:article_id>/edit', methods=['POST'])
@login_required
async def handle_edit(article_id: int):
    """处理文章编辑"""
    form_data = await request.form
    files = await request.files

    title = form_data.get('title', '').strip()
    category_id = form_data.get('category_id', type=int)
    content = form_data.get('content', '').strip()
    is_public = form_data.get('is_public') == 'on'

    if not title:
        await flash('文章标题不能为空', 'error')
        return redirect(url_for('admin.edit_form', article_id=article_id))
    if not category_id:
        await flash('请选择分类', 'error')
        return redirect(url_for('admin.edit_form', article_id=article_id))
    if not content:
        await flash('文章内容不能为空', 'error')
        return redirect(url_for('admin.edit_form', article_id=article_id))

    db_session = g.db_session
    image_id = None

    # 处理可选的封面图片
    if 'cover_image' in files and files['cover_image'].filename:
        user_id = get_current_user_id()
        image = await ImageService(db_session).upload(files['cover_image'], user_id)
        image_id = image.id

    article_service = ArticleService(db_session)
    await article_service.update(
        article_id=article_id,
        title=title,
        category_id=category_id,
        content=content,
        is_public=is_public,
        image_id=image_id
    )

    await flash('文章修改成功', 'success')
    return redirect(url_for('admin.article_list'))


@bp.route('/article/<int:article_id>/toggle-public', methods=['POST'])
@login_required
async def toggle_public(article_id: int):
    """切换文章公开状态"""
    article_service = ArticleService(g.db_session)
    await article_service.toggle_public(article_id)
    return redirect(url_for('admin.article_list'))


@bp.route('/article/<int:article_id>/toggle-recommended', methods=['POST'])
@login_required
async def toggle_recommended(article_id: int):
    """切换文章推荐状态"""
    article_service = ArticleService(g.db_session)
    await article_service.toggle_recommended(article_id)
    return redirect(url_for('admin.article_list'))


@bp.route('/article/<int:article_id>/update-category', methods=['POST'])
@login_required
async def update_category(article_id: int):
    """修改文章分类"""
    form_data = await request.form
    category_id = form_data.get('category_id', type=int)
    if category_id:
        article_service = ArticleService(g.db_session)
        await article_service.update_category(article_id, category_id)
    return redirect(url_for('admin.article_list'))


@bp.route('/categories')
@login_required
async def category_list():
    """分类列表"""
    db_session = g.db_session
    category_service = CategoryService(db_session)
    categories = await category_service.get_all()

    # 获取每个分类的文章数
    category_counts = {}
    for cat in categories:
        category_counts[cat.id] = await category_service.get_article_count(cat.id)

    return await render_template(
        'admin/category_list.html',
        categories=categories,
        category_counts=category_counts
    )


@bp.route('/category/create', methods=['POST'])
@login_required
async def category_create():
    """创建分类"""
    form_data = await request.form
    name = form_data.get('name', '').strip()
    if not name:
        await flash('分类名称不能为空', 'error')
        return redirect(url_for('admin.category_list'))

    category_service = CategoryService(g.db_session)
    await category_service.create(name)
    await flash('分类创建成功', 'success')
    return redirect(url_for('admin.category_list'))


@bp.route('/category/<int:category_id>/update', methods=['POST'])
@login_required
async def category_update(category_id: int):
    """修改分类名称"""
    form_data = await request.form
    name = form_data.get('name', '').strip()
    if not name:
        await flash('分类名称不能为空', 'error')
        return redirect(url_for('admin.category_list'))

    category_service = CategoryService(g.db_session)
    await category_service.update(category_id, name)
    await flash('分类修改成功', 'success')
    return redirect(url_for('admin.category_list'))


@bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
async def category_delete(category_id: int):
    """删除分类"""
    category_service = CategoryService(g.db_session)
    count = await category_service.get_article_count(category_id)
    if count > 0:
        await flash(f'该分类下还有 {count} 篇文章，无法删除', 'error')
        return redirect(url_for('admin.category_list'))

    await category_service.delete(category_id)
    await flash('分类删除成功', 'success')
    return redirect(url_for('admin.category_list'))
