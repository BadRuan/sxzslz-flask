from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Category


class CategoryCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_categories(self) -> List[Category]:
        stmt = (
            select(Category)
            .order_by(Category.id)
            )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_public_categories(self) -> List[Category]:
        stmt = (
            select(Category)
            .where(Category.is_public == True)
            .order_by(Category.id)
            )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_category(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.commit()
        return category
