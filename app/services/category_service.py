from typing import Optional, List, Tuple, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Category
from app.crud import CategoryCrud


class CategoryService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.crud = CategoryCrud(session)

    async def get_all(self) -> List[Category]:
        return await self.crud.get_all_categories()