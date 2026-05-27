from datetime import datetime
from sqlalchemy import Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from .base import Base


class Category(Base):
    __tablename__: str = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description = mapped_column(Text)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())