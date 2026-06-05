# SXZSLZ - 沈巷镇水利站新闻管理系统

基于 Quart (异步 Flask) 构建的全栈新闻资讯管理系统，支持文章管理、图片上传、用户认证等功能。

## 技术栈

- **后端框架**: Quart (异步 Flask)
- **数据库**: PostgreSQL + asyncpg
- **ORM**: SQLAlchemy 2.0 (异步模式)
- **数据库迁移**: Alembic
- **模板引擎**: Jinja2
- **图片处理**: Pillow
- **Markdown**: Mistune + Pygments
- **密码加密**: Argon2
- **前端**: Tailwind CSS
- **运行环境**: Python 3.12+

## 功能特性

### 用户系统
- 用户登录/登出
- 密码加密存储 (Argon2)
- 登录状态管理 (Session)
- 登录验证装饰器

### 文章管理
- 文章分类管理
- 文章发布
- Markdown 转 HTML 渲染 (支持代码高亮)
- 文章分页浏览
- 文章阅读统计

### 图片管理
- 图片上传 (支持 PNG, JPG, JPEG, GIF, WebP)
- 图片自动压缩 (JPEG quality=85)
- 图片信息记录 (尺寸、大小、MIME类型)
- 图片访问服务

## 项目结构

```
sxzslz-flask/
├── app/
│   ├── __init__.py          # 应用工厂函数
│   ├── settings.py          # 配置管理 (Pydantic Settings)
│   ├── database.py          # 数据库连接管理
│   ├── models/              # 数据模型
│   │   ├── base.py          # SQLAlchemy Base
│   │   ├── user.py          # 用户模型
│   │   ├── article.py       # 文章/内容模型
│   │   ├── category.py      # 分类模型
│   │   └── image.py         # 图片模型
│   ├── crud/                # 数据库操作层
│   │   ├── user_crud.py
│   │   ├── article_crud.py
│   │   ├── category_crud.py
│   │   └── image_crud.py
│   ├── views/               # 路由视图
│   │   ├── auth.py          # 认证相关路由
│   │   ├── home.py          # 首页路由
│   │   ├── news.py          # 新闻列表/详情路由
│   │   ├── image.py         # 图片上传/访问路由
│   │   └── user.py          # 用户管理路由
│   ├── services/            # 业务逻辑层
│   │   ├── article_service.py
│   │   └── category_service.py
│   ├── utils/               # 工具函数
│   │   ├── auth.py          # 登录验证装饰器
│   │   └── markdown.py      # Markdown 处理
│   └── templates/           # Jinja2 模板
│       ├── common/          # 公共模板 (base, header, footer)
│       ├── auth/            # 登录页面
│       ├── home.html        # 首页
│       ├── news/            # 新闻列表/详情
│       └── user/            # 用户管理
├── alembic/                 # 数据库迁移文件
├── uploads/                 # 上传文件存储目录
├── main.py                  # 应用入口
├── test.py                  # 测试脚本
├── pyproject.toml           # 项目依赖配置
└── .env                     # 环境变量配置
```

## 快速开始

### 环境要求

- Python 3.12+
- PostgreSQL 数据库

### 安装依赖

```bash
# 使用 uv (推荐)
uv sync

# 或使用 pip
pip install -e .
```

### 配置环境变量

创建 `.env` 文件:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
DB_ECHO=False
DEBUG=True
SECRET_KEY=your-secret-key-here
```

### 初始化数据库

```bash
# 运行 Alembic 迁移
alembic upgrade head
```

或使用测试脚本初始化：

```bash
python test.py
```

### 启动应用

```bash
python main.py
```

应用将在 `http://0.0.0.0:8989` 启动。

## API 路由

| 路由 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 首页 |
| `/login` | GET/POST | 用户登录 |
| `/logout` | GET | 用户登出 |
| `/users` | GET | 用户列表 |
| `/news/list/` | GET | 新闻列表 |
| `/news/list/<category_id>` | GET | 分类新闻列表 |
| `/news/article/<article_slug>` | GET | 新闻详情 |
| `/image/upload` | POST | 图片上传 |
| `/image/<id>` | GET | 获取图片信息 |
| `/image/<filename>` | GET | 访问图片 |

## 数据库模型

### User (用户)
- `id`: 主键 (UUID, 32位)
- `username`: 用户名 (唯一)
- `nickname`: 昵称 (唯一)
- `password_hash`: 密码哈希 (Argon2)
- `create_at`/`update_at`: 时间戳

### Article (文章)
- `id`: 主键 (自增)
- `slug`: URL友好标识 (唯一, 自动生成)
- `title`: 标题
- `is_public`: 是否公开
- `view_count`: 浏览次数
- `category_id`: 分类外键
- `user_id`: 作者外键
- `create_at`/`update_at`: 时间戳

### Content (文章内容)
- `id`: 主键 (关联文章)
- `markdown`: Markdown 原文
- `html`: 渲染后 HTML

### Category (分类)
- `id`: 主键 (自增)
- `name`: 分类名称 (唯一)
- `description`: 描述
- `create_at`: 创建时间

### Image (图片)
- `id`: 主键 (自增)
- `filename`: 存储文件名
- `original_filename`: 原始文件名
- `file_size`: 文件大小
- `mime_type`: MIME 类型
- `width`/`height`: 图片尺寸
- `upload_time`: 上传时间

## 开发说明

### 初始化数据

```bash
# 创建数据库表
python test.py

# 添加测试用户和分类
python -c "
import asyncio
from app.database import get_async_db
from app.models import User
from app.crud import UserCrud
from app.services import CategoryService

async def init():
    async with get_async_db() as session:
        # 创建管理员
        crud = UserCrud(session)
        user = User.create_user('admin', '管理员', 'admin123', 'admin123')
        await crud.create_user(user)

        # 创建分类
        service = CategoryService(session)
        await service.create_category('通知公告', '')
        await service.create_category('泵站新闻', '')

asyncio.run(init())
"
```

### 数据库迁移

```bash
# 生成迁移文件
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head
```

## License

MIT
