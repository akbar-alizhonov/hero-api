import os.path
import sys

from loguru import logger

from src.config.settings import get_settings


def setup_logger(logs_directory: str = "logs"):
    logger.remove()
    log_format = (
        '{{"asctime": "{time:YYYY-MM-DD HH:mm:ss}", '
        '"level_name": "{level.name}, "name": "{name}", "message": "{message}"}}'
    )

    settings = get_settings()
    if not settings.logging.DEVELOPMENT:

        if not os.path.exists(logs_directory):
            os.makedirs(logs_directory)

        logger.add(
            os.path.join(logs_directory, "hero_api_logs_{time:YYYY-MM-DD}.json"),
            format=log_format,
            rotation="00:00",
            retention="10 days",
            compression="zip",
            level=settings.logging.LOG_LEVEL,
        )

    logger.add(
        sys.stderr,
        format=log_format,
        level=settings.logging.LOG_LEVEL,
    )
