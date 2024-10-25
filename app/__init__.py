from .logger import logger as logger_app  # noqa
from .celery import app as celery_app

__all__ = ('celery_app', 'logger_app')
