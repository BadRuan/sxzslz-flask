from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Category
from app.crud import CategoryCrud


class CategoryService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.crud = CategoryCrud(session)

    async def create_category(self, name: str) -> Category:
        category = Category(name=name)
        return await self.crud.create_category(category)

    async def get_all_categories(self) -> List[Category]:
        return await self.crud.get_all_categories()