from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List
from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base import Base

if TYPE_CHECKING:
    from .article import Article


class Category(Base):
    __tablename__: str = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    create_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    articles: Mapped[List[Article]] = relationship("Article", back_populates="category")

    def __repr__(self) -> str:
        return f"<Category {self.name}>"

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "create_at": self.create_at
        }
