from typing import List
from sqlalchemy import select
from app.database import get_async_db
from app.models import User


async def get_all_users() -> List[User]:
    async with get_async_db() as db:
        stmt = select(User).order_by(User.created)
        result = await db.execute(stmt)
        r = result.scalars().all()
        return list(r)

async def create_user(user: User) -> User:
    async with get_async_db() as s:
        s.add(user)
        return user
