from typing import Optional, List, Tuple, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import markdown_to_html
from app.models import Article, Content
from app.crud import ArticleCrud

class ArticleService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.crud = ArticleCrud(session)

    async def create(self,
                            category_id: int,
                            user_id: str,
                            title: str,
                            image_id: Optional[int],
                            content: str,
                            is_public: bool = True
                        ) -> Article:
        article = Article(
            title=title,
            category_id=category_id,
            user_id=user_id,
            image_id=image_id,
            is_public=is_public
        )
        html = markdown_to_html(content)
        c = Content(markdown=content, html=html)
        a = await self.crud.create(article, c)
        return a

    async def update(self, article_id: int, title: str, category_id: int,
                     content: str, is_recommended: bool, image_id: Optional[int] = None) -> None:
        html = markdown_to_html(content)
        await self.crud.update(article_id, title, category_id, content, html, is_recommended, image_id) # type: ignore

    async def get_detail(self, article_slug: str) -> Optional[Article]:
        detail = await self.crud.get_article_by_slug(article_slug)
        if detail is not None:
            await self.crud.record_view(article_slug)
        return detail

    async def get_paginated(self, category_id: int, page: int, per_page: int) -> Tuple[List[Article], Dict]:
        per_page = min(per_page, 50)
        return await self.crud.get_paginated(
            page=page, per_page=per_page, category_id=category_id
        )

    async def get_admin_paginated(self,user_id: str, page: int, per_page: int) -> Tuple[List[Article], Dict]:
        per_page = min(per_page, 50)
        return await self.crud.get_admin_paginated(user_id=user_id, page=page, per_page=per_page)

    async def get_latest(self, limit: int) -> List[Article]:
        return await self.crud.get_latest(limit)

    async def get_user_latest(self, user_id: str, limit: int) -> List[Article]:
        return await self.crud.get_user_latest(user_id, limit)

    async def get_recommended(self, limit: int) -> List[Article]:
        return await self.crud.get_recommended(limit)

    async def get_counts(self) -> int:
        return await self.crud.get_counts()

    async def get_monthly_count(self) -> int:
        return await self.crud.get_monthly_count()

    async def toggle_public(self, article_id: int) -> None:
        await self.crud.toggle_public(article_id)

    async def toggle_recommended(self, article_id: int) -> None:
        await self.crud.toggle_recommended(article_id)

    async def update_category(self, article_id: int, category_id: int) -> None:
        await self.crud.update_category(article_id, category_id)
