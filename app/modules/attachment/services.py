from typing import Optional
from werkzeug.utils import secure_filename
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Attachment
from app.modules.attachment.crud import AttachmentCrud
from app.utils import generate_unique_filename


class AttachmentService:
    def __init__(self, session: AsyncSession) -> None:
        self.crud = AttachmentCrud(session)

    async def get_by_filename(self, filename: str) -> Optional[Attachment]:
        return await self.crud.get_by_filename(filename)

    async def save(self, file_name: str, file_size: int) -> Attachment:
        original_filename = secure_filename(file_name)
        filename = generate_unique_filename(original_filename)
        attachment = Attachment(
            filename=filename,
            original_filename=original_filename,
            file_size=file_size,
        )
        return await self.crud.save(attachment)

    async def get_counts(self) -> int:
        return await self.crud.get_counts()

    async def record_download(self, filename: str) -> None:
        await self.crud.record_download(filename)
