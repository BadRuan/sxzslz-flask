from sxzslz.model import DatabaseConfig
from sxzslz.config.settings import DATABASE_DEV


def get_database_config() -> DatabaseConfig:
    return DATABASE_DEV
