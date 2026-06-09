from typing import Dict
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.models import Base, User



class Attachment(Base):
    __tablename__: str = "attachments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    # 存储的文件名
    filename: Mapped[str] = mapped_column(String(200), nullable=False)
    # 原始文件名
    original_filename: Mapped[str] = mapped_column(String(200), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    # 上传用户
    user_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    # 下载次数
    download_count: Mapped[int] = mapped_column(Integer, default=0)
    upload_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    user: Mapped[User] = relationship(
        "User",
        back_populates="attachments"
    )

    def __repr__(self) -> str:
        return f"<Attachment {self.filename}>"

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'upload_time': self.upload_time,
            'url': f'/attachment/{self.filename}',
            'download_count': self.download_count
        }
        