from quart import Blueprint, render_template, g
from app.crud import UserCrud


bp = Blueprint('user', __name__)

@bp.route('/users')
async def users():
    crud = UserCrud(g.db_session)
    users = await crud.get_all_users()
    return await render_template('user/user_list.html', users=users)
