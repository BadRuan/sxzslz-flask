from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models import Attachment


class AttachmentCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def get_by_filename(self, filename: str) -> Optional[Attachment]:
        result = await self.session.execute(
            select(Attachment)
            .where(Attachment.filename == filename)
        )
        return result.scalar_one_or_none()
    
    async def save_attachment(self, attachment: Attachment) -> Attachment:
        self.session.add(attachment)
        await self.session.flush()
        return attachment
    
    async def get_counts(self) -> int:
        return await self.session.scalar(
            func.count(Attachment.id)
        )