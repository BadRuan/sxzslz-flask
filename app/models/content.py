from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Dict
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base
if TYPE_CHECKING:
    from .article import Article

class Content(Base):
    __tablename__: str = "contents"

    id: Mapped[int] = mapped_column(ForeignKey('articles.id'), primary_key=True)
    markdown: Mapped[str] = mapped_column(Text, nullable=False)
    html: Mapped[str] = mapped_column(Text)
    
    article: Mapped[Article] = relationship(
        "Article",
        back_populates="content"
    )
    
    def __repr__(self) -> str:
        return f"<Conent {self.id}>"
    
    def to_dict(self) -> Dict:
        return {
            "内容编号": self.id,
            "Markdown内容": self.markdown[:100] + "..." if len(self.markdown) > 100 else self.markdown,
            "HTML内容长度": len(self.html) if self.html else 0
        }