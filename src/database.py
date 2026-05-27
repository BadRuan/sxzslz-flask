from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .settings import settings


async_engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True, 
    pool_pre_ping=True
    )

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
    )

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def init_db() -> None:
    from .models.base import Base
    from .models import User, Category, Post, PostContent

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    