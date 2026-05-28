from app.database import init_db
from app.models import User, Category, Article, Content
from app.crud import  create_user, create_category, get_all_categories, create_article, get_latest_article

async def init_db_() -> None:
    await init_db()
    print('初始化数据库,创建数据表')

async def insert_init_data() -> None:
    # user: User = User(username='admin',nickname='管理员', password_hash='d033e22ae348aeb5660fc2140aec35850c4da997')
    # await create_user(user)
    # print(f'已创建默认用户 {user.nickname}')
    # categories = [
    #     ('文章草稿', '待发布的文章', False),
    #     ('私密文章', '需要和谐不予公开的内容', False),
    #     ('本站新闻', '沈巷镇水利站新闻、领导视察等', True),
    #     ('通知公告', '沈巷镇水利站日常发布的通知内容', True),
    #     ('工程招标', '沈巷镇水利站招投标文件等', True),
    #     ('文件公示', '沈巷镇水利站文件公示等', True),
    #     ('泵站风采', '沈巷镇水利站照片等', True)
    # ]
    # for c in categories:
    #     category = Category(name=c[0], description=c[1], is_public=c[2])
    #     await create_category(category)
    # for c in await get_all_categories():
    #     print(f"成功创建分类： {c.name}")
    post = Article(
        category_id=4, 
        user_id=1,
        title='测试文章45',
        is_public=True,
    )
    content = Content(
        markdown='#测试文章1231', 
        html='<html>'
    )
    p = await create_article(post, content)
    print(f'成功创建文章{p.id}')

async def test_get_latest_article() -> None:
    for a in await get_latest_article(5):
        print(a.to_dict_with_relations())