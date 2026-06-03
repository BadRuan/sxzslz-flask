from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import markdown_to_html
from app.models import Article, Content
from app.crud import ArticleCrud, CategoryCrud

class ArticleService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.crud = ArticleCrud(session)
        
    async def create_article(self,
                             category_id: int,
                             user_id: int,
                             title: str,
                             content: str
                        ) -> Article:
        article = Article(
            title=title,
            category_id=category_id,
            user_id=user_id,
            is_public=True
        )
        html = markdown_to_html(content)
        c = Content(markdown=content, html=html)
        a = await self.crud.create_article(article, c)
        return a