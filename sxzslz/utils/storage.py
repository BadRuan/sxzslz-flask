from pymysql import connect, cursors
from sxzslz.utils.logger import Logger
from sxzslz.model import DatabaseConfig
from sxzslz.config.configuration import get_database_config


logger = Logger(__name__)


class Storage:
    def __init__(self):
        self.conn = None

    def _execute(self, sql: str, args: tuple):
        cursor = self.conn.cursor()  # type: ignore
        cursor.execute("SET time_zone= 'Asia/Shanghai';")  # 解决时区不一致问题
        if args == None:
            cursor.execute(sql)
            return cursor
        else:
            cursor.execute(sql, args)
            return cursor

    def query_one(self, sql: str, args: tuple):
        return self._execute(sql, args).fetchone()

    def query_all(self, sql: str, args: tuple):
        return self._execute(sql, args).fetchall()

    def save(self, sql: str, *args: tuple) -> bool:
        self._execute(sql, args)
        self.conn.commit()  # type: ignore
        return True

    def remove(self, sql: str, args: tuple) -> bool:
        return self.save(sql, args)

    def update(self, sql: str, args: tuple) -> bool:
        return self.save(sql, args)

    def __enter__(self):
        try:
            config: DatabaseConfig = get_database_config()
            self.conn = connect(
                host=config.url,
                port=config.port,
                user=config.user,
                password=config.password,
                database=config.database,
                charset="utf8mb4",
                cursorclass=cursors.DictCursor,
            )
            return self

        except Exception:
            logger.error(f"MySQL数据库异常: {Exception}")

    def __exit__(self, exc_type, exc, tb):
        self.conn.close()  # type: ignore
