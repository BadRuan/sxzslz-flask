from asyncio import run
from random import choice
from app.models import User
from app.utils import markdown_to_html
from app.services import ArticleService, CategoryService
from app.database import init_db, get_async_db
from app.crud import UserCrud, CategoryCrud

async def db_begin() -> None:
    await init_db()

async def test_markdown_to_html() -> None:
    markdown: str = """![](https://pandao.github.io/editor.md/images/logos/editormd-logo-180x180.png)

    """
    html = markdown_to_html(markdown)
    print(html)

async def test_create_article() ->None:
    async with get_async_db() as session:
        service = ArticleService(session)
        user_crud = UserCrud(session)
        markdwon:str = """## 一、出纳收支报销单

数据来源：
1. 本期账户收入：银行本月账户明细的收入
2. 本期账户支出：银行本月账户明细的支出
3. 国库集中支付：一体化系统的支出合计
4. 本期实际入账支出：一体化系统的支出合计
## 二、支付凭证单位生成查询支出明细表

在一体化系统，支付凭证模块根据 **清算日期** 筛选出目标月份清单，选择导出清单，梳理掉不需要的部分，形成每月支出明细表。
## 三、账户交易明细（流水）

登陆 徽商银行交易家平台 导出。
## 四、电子回单

登陆 徽商银行交易家平台 导出。
## 五、固定资产表

### 1、折旧/摊销总况表

操作流程：
折旧/摊销管理 -> 计提折旧/摊销列表 -> 选择账期 -> 打印折旧/摊销总况
### 2、月固定资产总表

需要附**月固定资产总表**，表格来自：固定资产  ->  查询中心 -> 实时总账查询，需要注意选择需要的时间。
"""
        category_crud = CategoryCrud(session)
        categories = await category_crud.get_all_categories()
        users = await user_crud.get_all_users()
        if not categories or not users:
            print("请先创建用户和分类")
            return
        category_ids = [c.id for c in categories]
        user_ids = [u.id for u in users]
        for i in range(1,1000):
            r = await service.create_article(choice(category_ids), choice(user_ids), f'测试文章{i}', '随便写的摘要', 1, markdwon)
            print(r)

async def test_add_user() -> None:
    async with get_async_db() as session:
        crud = UserCrud(session)
        for i in range(1,11):
            user = User.create_user(username=f'user_{i}', nickname=f'用户_{i}',password='admin',repeat_password='admin')
            u = await crud.create_user(user)
            print(u)

async def test_add_category() -> None:
    async with get_async_db() as session:
          service = CategoryService(session)
          await service.create_category('通知公告','')
          await service.create_category('文件公示','')
          await service.create_category('工程项目','')
          await service.create_category('泵站新闻','')

if __name__ == "__main__":
    run(test_create_article())