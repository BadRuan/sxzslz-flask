from flask import url_for
from math import ceil


class Paginator:
    def __init__(
        self, total: int, page: int, subset_id: int, per_page: int, endpoint, **kwargs
    ) -> None:
        self.total: int = total
        self.page: int = page
        self.per_page: int = per_page
        self.subset_id: int = subset_id
        self.endpoint = endpoint
        self.kwargs = kwargs

        # 总页数
        self.total_pages: int = max(ceil(total / per_page), 1) if total else 0

        # 校验当前页码
        self.page = max(1, min(page, self.total_pages))

    @property
    def has_prev(self) -> bool:
        return self.page > 1

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def prev_num(self) -> int:
        return self.page - 1

    @property
    def next_num(self) -> int:
        return self.page + 1

    def iter_pages(
        self,
        left_edge: int = 2,
        left_current: int = 1,
        right_current: int = 2,
        right_edge: int = 2,
    ):
        if self.total_pages == 0:
            return []

        # 计算需要显示的页码范围
        start: int = max(1, self.page - left_current)
        end: int = min(self.total_pages, self.page + right_current)

        # 补充两侧边缘页码
        if self.page - left_current > 1:
            start = max(1, start - left_edge)
        if self.page + right_current < self.total_pages:
            end = min(self.total_pages, end + right_edge)
        return range(start, end + 1)

    def get_page_url(self, page_num: int):
        return url_for(
            self.endpoint,
            page=page_num,
            subset_id=self.subset_id,
            limit=self.per_page,
            **self.kwargs,
        )
