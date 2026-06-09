from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Category
from app.crud import CategoryCrud


class CategoryService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.crud = CategoryCrud(session)

    async def create(self, name: str) -> Category:
        category = Category(name=name)
        return await self.crud.create_category(category)

    async def get_all(self) -> List[Category]:
        return await self.crud.get_all_categories()

    async def update(self, category_id: int, name: str) -> None:
        await self.crud.update_name(category_id, name)

    async def delete(self, category_id: int) -> bool:
        return await self.crud.delete_category(category_id)

    async def get_article_count(self, category_id: int) -> int:
        return await self.crud.get_article_count(category_id)