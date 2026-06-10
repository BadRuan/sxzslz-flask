from quart import Blueprint, render_template, g
from app.services import UserService


bp = Blueprint('user', __name__)

@bp.route('/users')
async def users():
    service = UserService(g.db_session)
    users = await service.get_all()
    return await render_template('user/user_list.html', users=users)
