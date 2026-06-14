from quart import Blueprint, request, g
from pydantic import TypeAdapter
from app.services import ArticleService, CategoryService
from app.schema.base import api_response, ArticleResponse, CategoryResponse


bp = Blueprint('article', __name__)

@bp.route('/list')
async def list(category_id: int = 1):
    session = g.db_session
    category_service = CategoryService(session)
    article_service = ArticleService(session)
    
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    categories = await category_service.get_all()
    article_list, pagination = await article_service.get_paginated(
        page=page,
        per_page=per_page,
        category_id=category_id
    )
    
    articles = [ArticleResponse.model_validate(article) for article in article_list]
    categories_data = [CategoryResponse.model_validate(item) for item in categories]
    return api_response(data={
        'categories': categories_data,
        'article_list': articles,
        'pagination': pagination
    })


@bp.route('/<article_slug>')
async def detail(article_slug: str):
    service = ArticleService(g.db_session)
    detail = await service.get_detail(article_slug)
    if detail is not None:
        return api_response(data=
            {
                'detail': ArticleResponse.model_validate(detail) 
            })
    else:
        return api_response(code=404)