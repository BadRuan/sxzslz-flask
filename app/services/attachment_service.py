from typing import Optional
from os import SEEK_END, path
from werkzeug.utils import secure_filename
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from app.settings import settings
from app.models import Attachment
from app.crud import AttachmentCrud


def generate_unique_filename(filename):
    """生成唯一文件名，防止冲突"""
    ext = filename.rsplit('.', 1)[1].lower()
    return f"{uuid4().hex}.{ext}"

class AttachmentService:
    def __init__(self, session: AsyncSession) -> None:
        self.crud = AttachmentCrud(session)
    
    async def get_by_filename(self, filename: str) -> Optional[Attachment]:
        return await self.crud.get_by_filename(filename)
    
    async def save_attachment(self, file_name: str, file_size: int) -> Attachment:
        # 安全处理文件名
        original_filename = secure_filename(file_name)
        # 生成唯一文件名
        filename = generate_unique_filename(original_filename)
        # 获取文件信息
        
        
        attachment = Attachment(
            filename=filename,
            original_filename=original_filename,
            file_size=file_size,
        )
        
        return await self.crud.save_attachment(attachment)

    async def get_counts(self) -> int:
        return await self.crud.get_counts()