from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Category, Article


class CategoryCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_categories(self) -> List[Category]:
        stmt = (
            select(Category)
            .order_by(Category.create_at)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, category_id: int) -> Optional[Category]:
        return await self.session.get(Category, category_id)

    async def create_category(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.flush()
        return category

    async def update_name(self, category_id: int, name: str) -> None:
        category = await self.session.get(Category, category_id)
        if category:
            category.name = name
            await self.session.flush()

    async def delete_category(self, category_id: int) -> bool:
        category = await self.session.get(Category, category_id)
        if category:
            await self.session.delete(category)
            await self.session.flush()
            return True
        return False

    async def get_article_count(self, category_id: int) -> int:
        return (await self.session.scalar(
            select(func.count(Article.id)).where(Article.category_id == category_id)
        )) or 0
