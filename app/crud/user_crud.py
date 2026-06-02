from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User


class UserCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_users(self) -> List[User]:
        stmt = select(User).order_by(User.created)
        result = await self.session.execute(stmt)
        r = result.scalars().all()
        return list(r)

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        return user
