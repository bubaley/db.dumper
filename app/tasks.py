from celery import shared_task
from loguru import logger

from managers.config_manager import ConfigManager
from managers.dump_manager import DumpManager


@shared_task(name='dump')
def dump(**kwargs):
    try:
        config = ConfigManager().get_config_by_name(kwargs['name'])
        DumpManager(config).process()
    except Exception as e:
        logger.warning({'event': 'DUMP_TASK', 'error': e})
