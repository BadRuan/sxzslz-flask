from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from sqlalchemy.orm import joinedload
from app.models import Attachment


class AttachmentCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_filename(self, filename: str) -> Optional[Attachment]:
        result = await self.session.execute(
            select(Attachment)
            .where(Attachment.filename == filename)
            .options(
                joinedload(Attachment.user)
            )
        )
        return result.scalar_one_or_none()

    async def save(self, attachment: Attachment) -> Attachment:
        self.session.add(attachment)
        await self.session.flush()
        return attachment

    async def get_counts(self) -> int:
        return (await self.session.scalar(
            func.count(Attachment.id)
        )) or 0

    async def record_download(self, filename: str) -> None:
        await self.session.execute(
            update(Attachment)
            .where(Attachment.filename == filename)
            .values(download_count=Attachment.download_count + 1)
        )
        await self.session.flush()
