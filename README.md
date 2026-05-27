# Readme

## 技术栈

- 编程语言：Python
- 数据库：PostgreSQL
- 数据库ORM：sqlalchemy
- Web框架：Flask
- 前端库：Tailwindcss

## 数据库语句备忘

```sql
--- 建库
create database sxlslz;

-- 1. 用户表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    nickname VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

insert into users (username, nickname, password_hash) 
values
('admin','管理员', 'd033e22ae348aeb5660fc2140aec35850c4da997'),
('ruanfumin','阮福民', 'd033e22ae348aeb5660fc2140aec35850c4da997');

select * from users;

-- 2. 文章分类表
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    is_public BOOLEAN DEFAULT TRUE, -- TRUE: 公开显示; FALSE: 不公开显示（如“草稿”、“私有”）
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

insert into categories (name, description, is_public)
values
('文章草稿', '待发布的文章', false),
('私密文章', '需要和谐不予公开的内容', false),
('本站新闻', '沈巷镇水利站新闻、领导视察等', true),
('通知公告', '沈巷镇水利站日常发布的通知内容', true),
('工程招标', '沈巷镇水利站招投标文件等', true),
('文件公示', '沈巷镇水利站文件公示等', true),
('泵站风采', '沈巷镇水利站照片等', true);

select * from categories;
select * from categories where is_public is true;

-- 3. 文章主表 (元数据)
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    categories_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE cascade,
    title VARCHAR(200) NOT NULL,
    author INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- 状态控制
    is_public BOOLEAN DEFAULT FALSE, -- 文章是否公开
    view_count INTEGER DEFAULT 0,    -- 阅读量
    
    -- 时间记录
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

insert into posts 
(title, categories_id,author)
values 
('鸠江区水务局对沈巷镇水利站开展防溺水工作督查', 3,1);

select * from posts;


-- 4. 文章内容表 (Markdown 大文本分表)
CREATE TABLE post_contents (
    post_id INTEGER PRIMARY KEY REFERENCES posts(id) ON DELETE CASCADE,
    markdown_content TEXT NOT NULL, -- 存储 Markdown 源码
    html_content TEXT               -- 可选：预渲染的 HTML，减少服务器实时转换压力
);

insert into post_contents 
(post_id, markdown_content, html_content)
values
(1, '2025年7月30日区水务局对沈巷镇水利站开展防溺水工作督查', '<p>2025年7月30日区水务局对沈巷镇水利站开展防溺水工作督查</p>');

select * from post_contents where post_id = 1;

-- 6. 索引优化 (提高查询速度)
CREATE INDEX idx_posts_author ON posts(author);
CREATE INDEX idx_posts_created_at ON posts(created DESC);
CREATE INDEX idx_posts_is_public ON posts(is_public);
CREATE INDEX idx_categories_is_public ON categories(is_public);
```
