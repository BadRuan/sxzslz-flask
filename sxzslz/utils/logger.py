import logging
import sys
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler


def Logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 清除之前的处理器（防止重复）
    if logger.hasHandlers():
        logger.handlers.clear()

    # 创建日志目录
    log_dir = Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    # 控制台处理器
    console_format = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
    file_format = logging.Formatter(
        "%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s"
    )
    console_handler = logging.StreamHandler(sys.stdout)

    # 文件处理器（按天轮转）
    file_handler = TimedRotatingFileHandler(
        filename=log_dir / "app.log",
        when="midnight",  # 每天轮转
        backupCount=7,  # 保留7天
        encoding="utf-8",
    )

    # 设置文件和控制台日志显示级别
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)

    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
