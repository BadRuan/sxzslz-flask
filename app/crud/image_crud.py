from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Image


class ImageCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_filename(self, filename: str) -> Optional[Image]:
        result = await self.session.execute(
            select(Image)
            .where(Image.filename == filename)
        )
        return result.scalar_one_or_none()
    
    async def save_image(self, image: Image) -> Image:
        self.session.add(image)
        await self.session.flush()
        return image