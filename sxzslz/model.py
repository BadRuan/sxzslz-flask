from pydantic import BaseModel
from datetime import datetime


class DatabaseConfig(BaseModel):
    url: str
    port: int
    user: str
    password: str
    database: str


class User(BaseModel):
    user_id: int
    user_name: str
    nick_name: str
    password: str
    avatar_src: str
    create_time: datetime


class Subset(BaseModel):
    subset_id: int
    subset_name: str


class Article(BaseModel):
    article_id: int
    user_id: int
    subset_id: int
    title: str
    content: str | None
    create_time: datetime
    read_count: int
