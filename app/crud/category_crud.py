from typing import List
from sqlalchemy import select
from app.database import get_async_db
from app.models import Category


async def get_all_categories() -> List[Category]:
    async with get_async_db() as session:
        stmt = (
            select(Category)
            )
        
        result = await session.execute(stmt)
        return list(result.scalars().all())


async def get_public_categories() -> List[Category]:
    async with get_async_db() as session:
        stmt = (
            select(Category)
            .where(Category.is_public == True)
            )
        
        result = await session.execute(stmt)
        return list(result.scalars().all())

async def create_category(category: Category) -> Category:
    async with get_async_db() as s:
        s.add(category)
        return category
