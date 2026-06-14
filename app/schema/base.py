from typing import Optional, Dict,Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from quart import jsonify


def api_response(code=200, message:str = 'success', data=None):
    response = {
        "code": code,
        "message": message,
        "data": data or {}
    }
    return jsonify(response), code


def pagination(cur_page: int , page_size: int, total_size: int) -> Dict:
    # 1. 计算总页数 (向上取整)
    total_pages: int = (total_size + page_size - 1) // page_size if page_size > 0 else 0
    
    # 2. 边界保护：确保当前页码在合法范围内
    if cur_page < 1:
        cur_page = 1
    elif cur_page > total_pages and total_pages > 0:
        cur_page = total_pages
        
    # 3. 计算是否有上一页/下一页
    has_pre: bool = cur_page > 1
    has_next: bool = cur_page < total_pages
    
    # 4. 计算上一页/下一页的页码 (如果没有则为 None)
    pre_page: Optional[int] = cur_page - 1 if has_pre else None
    next_page: Optional[int] = cur_page + 1 if has_next else None
    
    return {
        'cur_page': cur_page,
        'page_size': page_size,
        'total_size': total_size,
        'has_pre': has_pre,
        'has_next': has_next,
        'pre_page': pre_page,
        'next_page': next_page
    }

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    nickname: str

class ImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    filename: str
    file_size: int
    mime_type: str
    
    user: Optional[UserResponse] = None

class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    slug: str
    is_public: bool
    view_count: int
    create_at: datetime
    update_at: datetime
    
    category: Optional[CategoryResponse] = None
    user: Optional[UserResponse] = None 

class ArticleDetailResponse(ArticleResponse):
    content: Optional[str] = None