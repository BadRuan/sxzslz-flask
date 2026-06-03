from asyncio import run
from app.database import AsyncSessionLocal
from app.utils import markdown_to_html
from app.services import ArticleService


async def test_markdown_to_html() -> None:
    markdown: str = """![](https://pandao.github.io/editor.md/images/logos/editormd-logo-180x180.png)
    
    """
    html = markdown_to_html(markdown)
    print(html)

async def test_create_article() ->None:
    session = AsyncSessionLocal()
    service = ArticleService(session)
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
    
    r = await service.create_aritcle(1, 1, '测试文章666', markdwon)
    print(r)

if __name__ == "__main__":
    run(test_create_article())