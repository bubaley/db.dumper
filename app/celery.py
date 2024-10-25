import os
import sys

from celery import Celery
from celery.schedules import crontab
from loguru import logger

from app.settings import Settings
from managers.config_manager import ConfigManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

settings = Settings()
BROKER_URL = str(settings.redis_dsn)

app = Celery(
    main='app',
    broker=BROKER_URL,
    broker_connection_retry_on_startup=True,
)
app.config_from_object('app.celery_config')
app.autodiscover_tasks(['app'])

configs = ConfigManager().configs
for el in configs:
    if not el.settings.schedule or not el.settings.schedule.active:
        continue
    schedule = el.settings.schedule.get_crontab_config()
    _schedule_string = ' '.join([str(v) for v in schedule.values()])
    app.conf.beat_schedule[el.name] = {
        'task': 'dump',
        'schedule': crontab(**schedule),
        'kwargs': {'name': el.name},
    }
    logger.info({'event': 'REGISTER', 'name': el.name, 'schedule': _schedule_string})
