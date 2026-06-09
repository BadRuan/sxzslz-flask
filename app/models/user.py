from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List
from datetime import datetime
from uuid import uuid4
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
from app.models import Base
if TYPE_CHECKING:
    from app.models import Article, Image, Attachment


ph = PasswordHasher(
    time_cost=3,       # 迭代次数
    memory_cost=65536, # 内存成本 (64 MB)
    parallelism=4      # 并行线程数
)

class User(Base):
    __tablename__: str = "users"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, index=True, default=lambda: uuid4().hex)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    nickname: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=func.now())
    update_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=func.now(), onupdate=func.now())

    articles: Mapped[List[Article]] = relationship(
        "Article",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    images: Mapped[List[Image]] = relationship(
        "Image",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    attachments: Mapped[List[Attachment]] = relationship(
        "Attachment",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    @classmethod
    def create_user(cls, username: str, nickname: str, password: str, repeat_password: str) -> User:
        if password != repeat_password:
            raise ValueError("两次密码不一致")
        hash = ph.hash(password)
        return cls(username=username, nickname=nickname, password_hash=hash)

    def check_password(self, plain_password: str) -> bool:
        try:
            ph.verify(self.password_hash, plain_password)
            return True
        except (VerifyMismatchError, InvalidHash):
            return False

    def __repr__(self) -> str:
        return f"<User {self.nickname}>"

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "create_at": self.create_at,
            "update_at": self.update_at
        }
