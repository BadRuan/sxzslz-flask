from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import markdown_to_html
from app.models import Article, Content
from app.crud import ArticleCrud


class ArticleService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.crud = ArticleCrud(session)

    async def create_article(self,
                            category_id: int,
                            user_id: str,
                            title: str,
                            summary: str,
                            image_id: int,
                            content: str
                        ) -> Article:
        article = Article(
            title=title,
            summary=summary,
            category_id=category_id,
            user_id=user_id,
            image_id=image_id
        )
        html = markdown_to_html(content)
        c = Content(markdown=content, html=html)
        a = await self.crud.create_article(article, c)
        return a

    async def get_article_detail(self, article_slug: str) -> Optional[Article]:
        detail = await self.crud.get_article_detail(article_slug)
        if detail is not None:
            await self.crud.recode_view(article_slug)
        return detail
