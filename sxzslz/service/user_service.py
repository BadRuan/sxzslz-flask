from sxzslz.model import User
from sxzslz.dao.user_dao import UserDao


class UserService:

    def __init__(self):
        self._dao: UserDao = UserDao()

    def add(
        self, user_name: str, nick_name: str, password: str, avatar_src: str
    ) -> bool:
        def is_not_empty(item: str) -> bool:
            if item.strip() == "":
                return False
            return True

        def any_not_empty(lst) -> bool:
            return all(is_not_empty(item) for item in lst)

        if any_not_empty([user_name, nick_name, password, avatar_src]):
            return self._dao.add(user_name, nick_name, password, avatar_src)
        else:
            return False

    def query_one(self, user_id: int) -> User | None:
        if user_id <= 0:
            return None
        else:
            return self._dao.query_one(user_id)
