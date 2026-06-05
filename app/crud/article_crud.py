from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func, update
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
        await self.session.flush()
        await self.session.refresh(article)
        return article

    async def get_latest_article(self, limit: int) -> List[Article]:
        stmt = (
            select(Article)
            .where(Article.is_public == True)
            .options(
                joinedload(Article.user),
                joinedload(Article.category)
            )
            .order_by(desc(Article.create_at))
            .limit(limit)
            )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_articles_paginated(
        self,
        page: int = 1,
        per_page: int = 10,
        category_id: Optional[int] = None
    ) -> Tuple[List[Article], int]:
        """分页查询文章，返回 (文章列表, 总数)"""
        # 基础查询条件
        base_query = select(Article).where(Article.is_public == True)
        if category_id is not None:
            base_query = base_query.where(Article.category_id == category_id)

        # 查询总数
        count_stmt = select(func.count()).select_from(base_query.subquery())
        total = (await self.session.execute(count_stmt)).scalar() or 0

        # 分页查询
        offset = (page - 1) * per_page
        stmt = (
            base_query
            .options(
                joinedload(Article.user),
                joinedload(Article.category)
            )
            .order_by(desc(Article.create_at))
            .offset(offset)
            .limit(per_page)
        )
        result = await self.session.execute(stmt)
        articles = list(result.scalars().all())

        return articles, total

    async def get_user_all_articles(self, user_id: str) -> List[Article]:
        stmt = (
            select(Article).where(Article.user_id == user_id).options(
                selectinload(Article.user)
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_article_detail(self, article_slug: str) -> Optional[Article]:
        stmt = (
            select(Article)
            .where(Article.slug==article_slug)
            .options(
                joinedload(Article.user),
                joinedload(Article.category),
                joinedload(Article.content)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def recode_view(self, article_slug: str) -> None:
        await self.session.execute(
            update(Article)
            .where(Article.slug==article_slug)
            .values(view_count = Article.view_count + 1)
        )
        await self.session.flush()
        