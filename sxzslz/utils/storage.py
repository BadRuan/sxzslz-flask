import pymysql
from dbutils.pooled_db import PooledDB
import pymysql.cursors
from sxzslz.utils.logger import Logger
from sxzslz.model import DatabaseConfig
from sxzslz.config.configuration import get_database_config


logger = Logger(__name__)


class Storage:
    _pool = None  # 连接池单例

    @classmethod
    def init_pool(cls):
        if cls._pool is None:
            config: DatabaseConfig = get_database_config()
            cls._pool = PooledDB(
                creator=pymysql,
                maxconnections=10,
                mincached=2,
                maxcached=5,
                host=config.url,
                port=config.port,
                user=config.user,
                password=config.password,
                database=config.database,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
            )
            logger.info("MySQL 连接池初始化完成")

    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            message: str = "连接池未初始化，请先调用 init_pool()"
            logger.error(message)
            raise RuntimeError(message)
        try:
            conn = cls._pool.connection()
            conn.ping(reconnect=True)
            return conn
        except Exception as e:
            logger.error(f"获取连接失败: {str(e)}")
            raise

    @classmethod
    def execute(cls, sql: str, params=None, autocommit=False):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            if not autocommit:
                conn.begin()
            cursor = conn.cursor()
            affected_rows = cursor.execute(sql, params or ())
            if not autocommit:
                conn.commit()
            logger.info(f"SQL 执行成功，影响行数: {affected_rows}")
            return affected_rows
        except Exception as e:
            if conn and not autocommit:
                conn.rollback()
            logger.error(f"SQL 执行失败: {sql}, 参数: {params}, 错误: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def query(cls, sql: str, params=None):
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            results = cursor.fetchall()
            logger.info(f"查询成功，返回 {len(results)} 条数据")
            return results
        except Exception as e:
            logger.error(f"查询失败: {sql}, 参数: {params}, 错误: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def close_pool(cls):
        if cls._pool:
            cls._pool.close()
            cls._pool = None
            logger.info("MySQL 连接池已关闭")

    # def __init__(self):
    #     self.conn = None

    # def _execute(self, sql: str, args: tuple):
    #     cursor = self.conn.cursor()  # type: ignore
    #     cursor.execute("SET time_zone= 'Asia/Shanghai';")  # 解决时区不一致问题
    #     if args == None:
    #         cursor.execute(sql)
    #         return cursor
    #     else:
    #         cursor.execute(sql, args)
    #         return cursor

    # def query_one(self, sql: str, args: tuple):
    #     return self._execute(sql, args).fetchone()

    # def query_all(self, sql: str, args: tuple):
    #     return self._execute(sql, args).fetchall()

    # def save(self, sql: str, *args: tuple) -> bool:
    #     self._execute(sql, args)
    #     self.conn.commit()  # type: ignore
    #     return True

    # def remove(self, sql: str, args: tuple) -> bool:
    #     return self.save(sql, args)

    # def update(self, sql: str, args: tuple) -> bool:
    #     return self.save(sql, args)

    # def __enter__(self):
    #     try:
    #         config: DatabaseConfig = get_database_config()
    #         self.conn = connect(
    #             host=config.url,
    #             port=config.port,
    #             user=config.user,
    #             password=config.password,
    #             database=config.database,
    #             charset="utf8mb4",
    #             cursorclass=cursors.DictCursor,
    #         )
    #         return self

    #     except Exception:
    #         logger.error(f"MySQL数据库异常: {Exception}")

    # def __exit__(self, exc_type, exc, tb):
    #     self.conn.close()  # type: ignore
