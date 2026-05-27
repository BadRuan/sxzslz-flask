from typing import List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Post
from src.utils import Logger


log = Logger(__name__)

async def get_latest_5_post(db: AsyncSession) -> List[Post]:
    stmt = (
        select(Post)
        .where(Post.is_public == True)
        .order_by(Post.created.desc())
        .options(
            selectinload(Post.category_ref),
            selectinload(Post.author_ref)
        )
        .limit(5)
        )
    
    result = await db.execute(stmt)
    return list(result.scalars().all())
