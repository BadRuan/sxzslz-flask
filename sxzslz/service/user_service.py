from sxzslz.dao import Dao
from sxzslz.dao.user_dao import UserDao
from sxzslz.service import Service


class UserService(Service):

    def __init__(self):
        super().__init__()
        self._dao: Dao = UserDao()

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

    def update(self, user_id: int, new_hashed_password: str) -> bool:
        if user_id <= 0:
            return False
        else:
            count: int = self.get_counts()
            if user_id > count:
                return False
        return self._dao.update(user_id, new_hashed_password)
