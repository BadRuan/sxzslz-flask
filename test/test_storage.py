import pytest
from src.utils import Storage, Logger

log = Logger(__name__)

@pytest.mark.asyncio
async def test_stroage_connect():
    async with Storage() as storage:
        log.info('Storage 连接测试成功.')
        assert storage != None
    