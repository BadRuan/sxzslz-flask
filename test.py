from asyncio import run
from os import path, listdir
from glob import glob
from random import choice
from app.models import User
from app.utils import markdown_to_html
from app.services import ArticleService, CategoryService
from app.database import init_db, get_async_db
from app.crud import UserCrud, CategoryCrud, ArticleCrud

async def db_begin() -> None:
    await init_db()

async def test_markdown_to_html() -> None:
    markdown: str = """![](https://pandao.github.io/editor.md/images/logos/editormd-logo-180x180.png)

    """
    html = markdown_to_html(markdown)
    print(html)

async def test_create_article() ->None:
    base_dir = '/Users/ruanfumin/Documents/sxzslz-flask/markdown'
    files = [file for file in listdir(base_dir)] 
    async with get_async_db() as session:
        service = ArticleService(session)
        for file in files:
            print(file)
            with open(path.join(base_dir, file), mode='r', encoding='utf-8') as f: 
                await service.create_article(
                    category_id=1, 
                    user_id='4ab6a3783df446cfb8517da843a5994a', 
                    title=file[:-3], 
                    summary='摘要', 
                    image_id=1, 
                    content=f.read()
                )

async def test_add_user() -> None:
    async with get_async_db() as session:
        crud = UserCrud(session)
        users = [
            ('admin', '系统管理员'),
            ('ruanfumin', '阮福民'),
            ('yuqingbin', '余庆斌'),
            ('zhouweijun', '周卫军'),
            ('liwei', '李伟'),
            ('liuguisheng', '刘桂胜'),
            ('wangjian', '王健'),
            ('chenbuming', '陈步明'),
            ('pengbixiang', '彭必祥'),
        ]
        for i in users:
            _pass = 'admin'
            user = User.create_user(username=i[0], nickname=i[1],password=_pass,repeat_password=_pass)
            u = await crud.create_user(user)
            print(u)

async def test_add_category() -> None:
    async with get_async_db() as session:
          service = CategoryService(session)
          l = [
              '单位简介',
              '水利站新闻',
              '通知公告',
              '会议记录',
              '文件公示',
              '财政信息',
              '工程项目',
              '人事招考',
              '信息转载'
            ]
          for i in l:
              await service.create_category(i)
                      
async def test_get_total_article_counts() -> None:
    async with get_async_db() as session:
        crud = ArticleCrud(session)
        count: int = await crud.get_counts()
        print(f'文章总数： {count}')


async def main():
    # await db_begin()
    # await test_add_category()
    # await test_add_user()
    await test_create_article()
    
if __name__ == "__main__":
    run(main())