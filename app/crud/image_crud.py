from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from sqlalchemy.orm import joinedload
from app.models import Image


class ImageCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_filename(self, filename: str) -> Optional[Image]:
        result = await self.session.execute(
            select(Image)
            .where(Image.filename == filename)
            .options(
                joinedload(Image.user)
            )
        )
        return result.scalar_one_or_none()

    async def save_image(self, image: Image) -> Image:
        self.session.add(image)
        await self.session.flush()
        return image

    async def get_counts(self) -> int:
        return (await self.session.scalar(
            func.count(Image.id)
        )) or 0

    async def record_view(self, filename: str) -> None:
        await self.session.execute(
            update(Image)
            .where(Image.filename == filename)
            .values(view_count = Image.view_count + 1)
        )
        await self.session.flush()
