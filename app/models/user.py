from typing import Dict
from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base import Base


class User(Base):
    __tablename__: str = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    nickname: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    articles = relationship(
        "Article", 
        back_populates="user", 
        cascade="all, delete-orphan",
        lazy="selectin"
        )

    def __repr__(self) -> str:
        return f"<User {self.nickname}>"
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "created": self.created,
            "updated": self.updated
        }
        