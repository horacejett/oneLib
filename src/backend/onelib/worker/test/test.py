from loguru import logger

from onelib.worker.main import onelib_celery


@onelib_celery.task
def add(x, y):
    logger.info(f"add {x} + {y}")
    return x + y
