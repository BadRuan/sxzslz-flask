from typing import Dict, List
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.models import Base, User, Article


class Image(Base):
    __tablename__: str = "images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    # 存储的文件名
    filename: Mapped[str] = mapped_column(String(200), nullable=False)
    # 原始文件名
    original_filename: Mapped[str] = mapped_column(String(200), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    # MIME类型
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    # 上传用户
    user_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    upload_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # 浏览次数
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    
    user: Mapped[User] = relationship(
        "User",
        back_populates="images",
        lazy="selectin"
    )

    articles: Mapped[List[Article]] = relationship(
        "Article",
        back_populates="image",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Image {self.filename}>"

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'upload_time': self.upload_time,
            'width': self.width,
            'height': self.height,
            'url': f'/image/{self.filename}',
            'view_count': self.view_count
        }
        