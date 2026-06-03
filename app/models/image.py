from typing import Dict
from datetime import datetime
from sqlalchemy import Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base import Base


class Image(Base):
    __tablename__: str = "images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # 存储的文件名
    filename: Mapped[str] = mapped_column(String(200), nullable=False)
    # 原始文件名
    original_filename = mapped_column(String(200), nullable=False)
    file_size = mapped_column(Integer, nullable=False)
    # MIME类型
    mime_type = mapped_column(String(100), nullable=False)
    upload_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    width = mapped_column(Integer)
    height = mapped_column(Integer)
    
    def __repr__(self) -> str:
        return f"<Image {self.file_name}>"
    
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
            'url': f'/images/{self.filename}'
        }
        