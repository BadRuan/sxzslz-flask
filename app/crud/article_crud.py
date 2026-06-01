from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload, joinedload
from app.database import get_async_db
from app.models import Article, Content


async def create_article(article: Article, content: Content) -> Article:
    async with get_async_db() as s:
        s.add(article)
        await s.flush()
        content.id = article.id
        s.add(content)
        await s.refresh(article)
        return article

async def get_latest_article(limit: int) -> List[Article]:
    async with get_async_db() as session:
        stmt = (
            select(Article)
            .where(Article.is_public == True) 
            .options(
                joinedload(Article.user),
                joinedload(Article.category)
            )
            .order_by(desc(Article.created))
            .limit(limit)
            )
        
        result = await session.execute(stmt)
        return list(result.scalars().all())

async def get_user_all_articles(user_id: int) -> List[Article]:
    async with get_async_db() as s:
        stmt = (
            select(Article).where(Article.user_id == user_id).options(
                selectinload(Article.author)
            )
        )
        result = await s.execute(stmt)
        return list(result.scalars().all())

async def get_article_detail(article_id: int) -> Optional[Article]:
    async with get_async_db() as s:
        stmt = (
            select(Article)
            .where(Article.id==article_id)
            .options(
                joinedload(Article.user),
                joinedload(Article.category),
                joinedload(Article.content)
            )
            )
        result = await s.execute(stmt)
        return result.scalar_one_or_none()