import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from rich.logging import RichHandler
from rich.traceback import install


def Logger(name: str):
	
    logger=logging.getLogger(name)
    install(show_locals=True) # 全局安装 rich 异常美化
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()


    log_dir = Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    console_handler = RichHandler(
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        level=logging.INFO
    )
    console_format = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
    file_format = logging.Formatter(
        "%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s"
    )
    console_handler.setFormatter(console_format)

    # 文件处理器（按天轮转）
    file_handler = TimedRotatingFileHandler(
        filename=log_dir / "app.log",
        when="midnight",  # 每天轮转
        backupCount=7,  # 保留7天
        encoding="utf-8",
    )
	
    # 设置文件和控制台日志显示级别
    file_handler.setLevel(logging.DEBUG)
    
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
