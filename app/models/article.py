from __future__ import annotations
from typing import TYPE_CHECKING, Dict
from datetime import datetime
from sqlalchemy import Integer, Text, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from . import Base
if TYPE_CHECKING:
    from .user import User
    from .category import Category
    

class Article(Base):
    __tablename__: str = "articles"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 外键
    category_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("categories.id", ondelete="CASCADE"), 
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False
    )

    # 关系映射
    user: Mapped[User] = relationship(
        "User", 
        back_populates="articles",
    )
    category: Mapped[Category] = relationship("Category",back_populates="articles")
    
    content: Mapped[Content] = relationship(
        "Content",
        back_populates="article", 
        uselist=False, 
        cascade="all, delete-orphan",
        lazy="select"
    )
    
    def __repr__(self) -> str:
        return f"<Article {self.title}>"
    
    def to_dict_with_relations(self) -> Dict:
        """包含用户和分类信息的字典表示"""
        return {
            "id": self.id,
            "title": self.title,
            "category_name": self.category.name if self.category else None,
            "author_nickname": self.user.nickname if self.user else None,
            "is_public": self.is_public,
            "view_count": self.view_count,
            "created": self.created,
            "updated": self.updated
        }

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
        return f"<Content {self.id}>"
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "markdown_preview": self.markdown[:100] + "..." if len(self.markdown) > 100 else self.markdown,
            "html_length": len(self.html) if self.html else 0
        }