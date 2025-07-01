from abc import ABCMeta
from abc import abstractmethod
from typing import List, TypeVar

T = TypeVar("T")


class Service(metaclass=ABCMeta):

    def __init__(self) -> None:
        self._dao = None

    @abstractmethod
    def add(self, *args, **kwargs) -> bool: ...

    def remove(self, id: int) -> bool:
        if id <= 0:
            return False
        else:
            count: int = self.get_counts(0)
            if id > count:
                return False
        return self._dao.remove(id)  # type: ignore

    def update(self, *args, **kwargs) -> bool: ...

    def query_one(self, id: int) -> object | None:
        if id <= 0:
            return None
        else:
            count: int = self.get_counts(0)
            if id > count:
                return None
        return self._dao.query_one(id)  # type: ignore

    def query_by_page(self, page: int, limit: int):
        return self._dao.query_by_condition(page, limit)  # type: ignore

    def get_counts(self, id: int) -> int:
        return self._dao.get_counts(id)  # type: ignore
