from quart import Blueprint, render_template
from app.crud import get_all_users


bp = Blueprint('user', __name__)

@bp.route('/users')
async def users():
    users = await get_all_users()
    return await render_template('user/user_list.html', users=users)
