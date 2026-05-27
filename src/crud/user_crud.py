from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User
from src.utils import Logger


log = Logger(__name__)

async def get_admin_user(db: AsyncSession) -> Optional[User]:
    """
    获取管理员用户。
    如果找不到，返回 None。
    """
    # 构建查询语句，stmt 类型为 Select[Tuple[User]]
    stmt = select(User).where(User.username == "admin")
    
    # 执行查询，result 类型为 Result[Tuple[User]]
    result = await db.execute(stmt)
    
    # scalar_one_or_none 返回 Optional[User]
    admin: Optional[User] = result.scalar_one_or_none()
    
    # 类型守卫：处理 None 情况
    if admin is None:
        log.error("Admin user not found.")
        return None
    
    # 此时 Pylance 知道 admin 是 User 类型，可以安全访问 .nickname
    print(f"Found admin: {admin.nickname}")
    return admin
