from __future__ import annotations
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .settings import settings


async_engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=settings.DB_ECHO,          # 生产环境应通过配置控制
    pool_pre_ping=True,             # 自动检测并替换失效连接
    pool_size=20,                   # 常驻连接数，根据实际并发调整
    max_overflow=10,                # 超出 pool_size 后允许额外创建的连接数
    pool_timeout=30,                # 获取连接超时秒数
    pool_recycle=1800,              # 连接回收时间(秒)，防止数据库端主动断开
    pool_reset_on_return="commit",  # 归还连接时自动 commit/rollback
    )

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
    )

@asynccontextmanager
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
    from .models import User, Category, Article, Content

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    