from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Image
from app.crud import ImageCrud


class ImageService:
    def __init__(self, session: AsyncSession) -> None:
        self.crud = ImageCrud(session)

    async def get_by_filename(self, filename: str) -> Optional[Image]:
        return await self.crud.get_by_filename(filename)

    async def record_view(self, filename: str) -> None:
        await self.crud.record_view(filename)

    async def save(self, image: Image) -> Image:
        return await self.crud.save_image(image)

    async def get_counts(self) -> int:
        return await self.crud.get_counts()
