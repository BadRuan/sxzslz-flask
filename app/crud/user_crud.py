from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User


class UserCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_users(self) -> List[User]:
        stmt = select(User).order_by(User.create_at)
        result = await self.session.execute(stmt)
        r = result.scalars().all()
        return list(r)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user
