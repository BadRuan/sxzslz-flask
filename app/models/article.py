from __future__ import annotations
from typing import TYPE_CHECKING, Dict
from datetime import datetime
from uuid import uuid4
from sqlalchemy import BigInteger, Integer, Text, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .category import Category


def generate_slug() -> str:
    """生成唯一的 slug"""
    return uuid4().hex[:16]


class Article(Base):
    __tablename__: str = "articles"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, default=generate_slug)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    create_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    update_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0)

    # 关系映射
    user: Mapped[User] = relationship(
        "User",
        back_populates="articles"
    )
    category: Mapped[Category] = relationship("Category", back_populates="articles")

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
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "category_name": self.category.name if self.category else None,
            "author_nickname": self.user.nickname if self.user else None,
            "is_public": self.is_public,
            "view_count": self.view_count,
            "create_at": self.create_at,
            "update_at": self.update_at
        }


class Content(Base):
    __tablename__: str = "contents"

    id: Mapped[int] = mapped_column(ForeignKey('articles.id'), primary_key=True)
    markdown: Mapped[str] = mapped_column(Text, nullable=False)
    html: Mapped[str] = mapped_column(Text, nullable=True)

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
