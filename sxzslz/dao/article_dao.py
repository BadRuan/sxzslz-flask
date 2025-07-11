from typing import List
from sxzslz.utils.logger import Logger
from sxzslz.utils.storage import Storage
from sxzslz.model import User, Subset, Article
from sxzslz.dao import Dao
from sxzslz.dao.subset_dao import SubsetDao
from sxzslz.dao.user_dao import UserDao


table_name: str = "article"
primary_key_name: str = "article_id"
logger = Logger(__name__)


class ArticleDao(Dao):

    def __init__(self):
        super().__init__(table_name, primary_key_name)

    def add(self, subset_id: int, user_id: int, title: str, content: str) -> bool:
        sql: str = f"""INSERT INTO {self.table_name}
                    (subset_id, user_id, title, content) 
                    VALUES (%s, %s, %s, %s)"""
        affected_rows: int = Storage.execute(
            sql, params=(subset_id, user_id, title, content)
        )
        if 1 == affected_rows:
            return True
        else:
            return False

    def update(self, article_id: int, title: str, content: str):
        sql: str = f"""UPDATE {self.table_name}
                            SET title = %s, content = %s
                            WHERE article_id = '{article_id}'"""
        affected_rows: int = Storage.execute(sql, params=(title, content))
        return affected_rows

    def add_read_count(self, article_id: int):
        sql: str = (
            f"UPDATE {self.table_name} SET read_count = read_count + 1 WHERE article_id = %s"
        )
        affected_rows: int = Storage.execute(sql, params=(article_id,))
        return affected_rows

    def query_one(self, article_id: int) -> Article | None:
        sql: str = f"SELECT * FROM {self.table_name} WHERE article_id = %s"
        result = Storage.query(sql, params=(article_id,))
        if () == result:
            return None
        else:
            result = result[0]
            subset_dao: Dao = SubsetDao()
            user_dao: Dao = UserDao()
            subset: Subset | None = subset_dao.query_one(result["subset_id"])
            user: User | None = user_dao.query_one(result["user_id"])
            return Article(
                article_id=int(result["article_id"]),
                subset_id=int(result["subset_id"]),
                user_id=int(result["user_id"]),
                title=result["title"],
                content=result["content"],
                create_time=result["create_time"],
                read_count=result["read_count"],
            )

    def get_counts(self, subset_id: int) -> int:  # type: ignore
        sql: str = (
            f"SELECT COUNT(*) AS count FROM {self.table_name} WHERE subset_id = %s"
        )
        result: int = Storage.query(sql, (subset_id,))[0]["count"]
        return result

    def query_by_condition(
        self, subset_id: int, page: int, limit: int
    ) -> List[Article]:
        offset: int = (page - 1) * limit
        sql: str = (
            f"SELECT * FROM {self.table_name} WHERE subset_id = %s ORDER BY create_time DESC LIMIT %s OFFSET %s"
        )
        results = Storage.query(
            sql,
            params=(
                subset_id,
                limit,
                offset,
            ),
        )
        return [
            Article(
                article_id=int(item["article_id"]),
                subset_id=int(item["subset_id"]),
                user_id=int(item["user_id"]),
                title=item["title"],
                content=None,
                create_time=item["create_time"],
                read_count=item["read_count"],
            )
            for item in results
        ]
