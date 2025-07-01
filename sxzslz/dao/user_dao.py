from typing import List
from sxzslz.dao import Dao
from sxzslz.utils.storage import Storage
from sxzslz.model import User
from sxzslz.utils.logger import Logger


logger = Logger(__name__)


class UserDao(Dao):

    def __init__(self):
        super().__init__("user", "user_id")

    def add(
        self, user_name: str, nick_name: str, password: str, avatar_src: str
    ) -> bool:
        sql: str = (
            f"""INSERT INTO {self.table_name}
                    (user_name, nick_name, password, avatar_src)
                    VALUES
                    (%s, %s, %s, %s)"""
        )
        affected_rows: int = Storage.execute(
            sql, params=(user_name, nick_name, password, avatar_src)
        )
        if 1 == affected_rows:
            return True
        else:
            return False

    def update(self, user_id: int, new_hashed_password: str) -> bool: ...

    def query_one(self, user_id: int) -> User | None:
        sql: str = f"SELECT * FROM {self.table_name} WHERE {self.primary_key_name} = %s"
        result = Storage.query(sql, params=(user_id,))
        if () == result:
            return None
        else:
            result = result[0]
            return User(
                user_id=int(result["user_id"]),
                user_name=result["user_name"],
                nick_name=result["nick_name"],
                password=result["password"],
                avatar_src=result["avatar_src"],
                create_time=result["create_time"],
            )

    def query_by_condition(self, page: int, limit: int) -> List[User]:
        offset: int = (page - 1) * limit
        sql: str = f"SELECT * FROM {self.table_name} LIMIT %s, %s"
        results = Storage.query(sql, params=(offset, limit))
        return [
            User(
                user_id=int(item["user_id"]),
                user_name=item["user_name"],
                nick_name=item["nick_name"],
                password=item["password"],
                avatar_src=item["avatar_src"],
                create_time=item["create_time"],
            )
            for item in results
        ]
