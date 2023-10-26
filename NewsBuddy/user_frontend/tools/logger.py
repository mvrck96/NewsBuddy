import os
import sys

from loguru import logger


LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    f"<blue>{os.getpid()}</blue> | "
    "<cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)


def create_logger(serialized: bool = False) -> logger:
    """Creates logger according to user settings.

    @param  serialized[bool]: Structured logging flag
            └─> default: True
    @return [logger]: Logger
    """
    logger.remove()
    logger.add(sys.stdout, serialize=serialized, format=LOG_FORMAT)
    logger.info(f"Logger initialized, structured logs: {serialized}")
    return logger


service_logger = create_logger()
