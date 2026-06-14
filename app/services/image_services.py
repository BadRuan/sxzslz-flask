from os import path, SEEK_END
from typing import Optional
from mimetypes import guess_type
from werkzeug.utils import secure_filename
from PIL import Image as PILImage
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Image
from app.crud.image_crud import ImageCrud
from app.settings import settings
from app.utils import generate_unique_filename


class ImageService:
    def __init__(self, session: AsyncSession) -> None:
        self.crud = ImageCrud(session)

    async def upload(self, file, user_id: str) -> Image:
        """统一的图片上传处理：校验、存储、生成记录"""
        original_filename = secure_filename(file.filename)
        filename = generate_unique_filename(original_filename)
        file_path = path.join(settings.IMAGE_UPLOAD_FOLDER, filename)

        file.seek(0, SEEK_END)
        file_size = file.tell()
        file.seek(0)

        mime_type = guess_type(filename)[0] or 'application/octet-stream'

        img = PILImage.open(file)
        width, height = img.size
        img = img.convert('RGB')
        img.save(file_path, 'JPEG', quality=85, optimize=True)

        image = Image(
            filename=filename,
            original_filename=original_filename,
            file_size=file_size,
            mime_type=mime_type,
            user_id=user_id,
            width=width,
            height=height,
        )
        return await self.crud.save_image(image)

    async def get_by_filename(self, filename: str) -> Optional[Image]:
        return await self.crud.get_by_filename(filename)

    async def record_view(self, filename: str) -> None:
        await self.crud.record_view(filename)

    async def save(self, image: Image) -> Image:
        return await self.crud.save_image(image)

    async def get_counts(self) -> int:
        return await self.crud.get_counts()
