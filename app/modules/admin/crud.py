from typing import List, Optional, Tuple
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func, update
from sqlalchemy.orm import joinedload
from app.models import Article, Content, Category, User


class ArticleCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, article: Article, content: Content) -> Article:
        self.session.add(article)
        await self.session.flush()
        content.id = article.id
        self.session.add(content)
        await self.session.flush()
        await self.session.refresh(article)
        return article

    async def get_latest(self, limit: int) -> List[Article]:
        """获取最新公开文章"""
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

    async def get_user_latest(self, user_id: str, limit: int) -> List[Article]:
        """获取指定用户的最新公开文章"""
        stmt = (
            select(Article)
            .where(Article.is_public == True, Article.user_id == user_id)
            .options(
                joinedload(Article.user),
                joinedload(Article.category)
            )
            .order_by(desc(Article.create_at))
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_paginated(
        self,
        page: int = 1,
        per_page: int = 10,
        category_id: Optional[int] = None
    ) -> Tuple[List[Article], int]:
        """分页查询公开文章"""
        base_query = select(Article).where(Article.is_public == True)
        if category_id is not None:
            base_query = base_query.where(Article.category_id == category_id)

        count_stmt = select(func.count()).select_from(base_query.subquery())
        total = (await self.session.execute(count_stmt)).scalar() or 0

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

    async def get_user_paginated(
        self,
        user_id: str,
        page: int = 1,
        per_page: int = 10,
        category_id: Optional[int] = None
    ) -> Tuple[List[Article], int]:
        """分页查询指定用户的公开文章"""
        base_query = select(Article).where(Article.is_public == True, Article.user_id == user_id)
        if category_id is not None:
            base_query = base_query.where(Article.category_id == category_id)

        count_stmt = select(func.count()).select_from(base_query.subquery())
        total = (await self.session.execute(count_stmt)).scalar() or 0

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

    async def get_admin_paginated(
        self,
        user_id: str,
        page: int = 1,
        per_page: int = 10
    ) -> Tuple[List[Article], int]:
        """后台分页查询所有文章（含草稿）"""
        base_query = select(Article)
        count_stmt = select(func.count()).select_from(base_query.subquery())
        total = (await self.session.execute(count_stmt)).scalar() or 0
        offset = (page - 1) * per_page
        stmt = (
            base_query
            .where(Article.user_id == user_id)
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

    async def get_recommended(self, limit: int) -> List[Article]:
        """获取推荐文章"""
        stmt = (
            select(Article)
            .where(Article.is_recommended == True)
            .options(
                joinedload(Article.image)
            )
            .order_by(desc(Article.create_at))
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, article_id: int) -> Optional[Article]:
        """根据 ID 获取文章（含内容）"""
        stmt = (
            select(Article)
            .where(Article.id == article_id)
            .options(
                joinedload(Article.content)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, article_id: int, title: str, category_id: int,
                     content: str, html: str, is_public: bool,
                     image_id: Optional[int] = None) -> None:
        """更新文章"""
        stmt = (
            select(Article)
            .where(Article.id == article_id)
            .options(joinedload(Article.content))
        )
        result = await self.session.execute(stmt)
        article = result.scalar_one_or_none()
        if article:
            article.title = title
            article.category_id = category_id
            article.is_public = is_public
            if image_id is not None:
                article.image_id = image_id
            if article.content:
                article.content.markdown = content
                article.content.html = html
            await self.session.flush()

    async def get_article_by_slug(self, article_slug: str) -> Optional[Article]:
        """根据 slug 获取文章详情"""
        stmt = (
            select(Article)
            .where(Article.slug == article_slug)
            .options(
                joinedload(Article.user),
                joinedload(Article.category),
                joinedload(Article.content)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def record_view(self, article_slug: str) -> None:
        """阅读量 +1"""
        await self.session.execute(
            update(Article)
            .where(Article.slug == article_slug)
            .values(view_count=Article.view_count + 1)
        )
        await self.session.flush()

    async def get_counts(self) -> int:
        return (await self.session.scalar(
            func.count(Article.id)
        )) or 0

    async def get_monthly_count(self) -> int:
        """获取本月文章数"""
        now = datetime.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return (await self.session.scalar(
            select(func.count(Article.id))
            .where(
                Article.create_at >= start_of_month
            )
        )) or 0

    async def toggle_public(self, article_id: int) -> None:
        article = await self.session.get(Article, article_id)
        if article:
            article.is_public = not article.is_public
            await self.session.flush()

    async def toggle_recommended(self, article_id: int) -> None:
        article = await self.session.get(Article, article_id)
        if article:
            article.is_recommended = not article.is_recommended
            await self.session.flush()

    async def update_category(self, article_id: int, category_id: int) -> None:
        article = await self.session.get(Article, article_id)
        if article:
            article.category_id = category_id
            await self.session.flush()


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


class UserCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_users(self) -> List[User]:
        stmt = select(User).order_by(User.create_at)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return list(users)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_count(self) -> int:
        return (await self.session.scalar(
            func.count(User.id)
        )) or 0
