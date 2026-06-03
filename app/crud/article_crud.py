from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload, joinedload
from app.models import Article, Content


class ArticleCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_article(self, article: Article, content: Content) -> Article:
        self.session.add(article)
        await self.session.flush()
        content.id = article.id
        self.session.add(content)
        await self.session.refresh(article)
        await self.session.commit()
        return article

    async def get_latest_article(self, limit: int) -> List[Article]:
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
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_user_all_articles(self, user_id: int) -> List[Article]:
        stmt = (
            select(Article).where(Article.user_id == user_id).options(
                selectinload(Article.author)
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_article_detail(self, article_id: int) -> Optional[Article]:
        stmt = (
            select(Article)
            .where(Article.id==article_id)
            .options(
                joinedload(Article.user),
                joinedload(Article.category),
                joinedload(Article.content)
            )
            )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()