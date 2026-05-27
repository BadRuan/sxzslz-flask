from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from .base import Base


class Post(Base):
    __tablename__: str = "posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    categories_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    author: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
