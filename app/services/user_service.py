from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.crud import UserCrud


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.crud = UserCrud(session)

    async def get_all(self) -> List[User]:
        return await self.crud.get_all_users()

    async def get_by_username(self, username: str) -> Optional[User]:
        return await self.crud.get_user_by_username(username)

    async def get_count(self) -> int:
        return await self.crud.get_count()
