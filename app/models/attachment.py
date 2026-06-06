from typing import Dict
from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from .base import Base



class Attachment(Base):
    __tablename__: str = "attachments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    # 存储的文件名
    filename: Mapped[str] = mapped_column(String(200), nullable=False)
    # 原始文件名
    original_filename: Mapped[str] = mapped_column(String(200), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    upload_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"<Attachment {self.filename}>"

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'upload_time': self.upload_time,
            'url': f'/attachment/{self.filename}'
        }
        