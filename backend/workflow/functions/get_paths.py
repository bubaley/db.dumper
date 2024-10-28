import os
import secrets
from datetime import datetime

from django.conf import settings

from config.models import Config


def get_dump_filename():
    date = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f'dump_{date}_{secrets.token_hex(nbytes=3)}.sql'


def get_config_dump_folder_path(config: Config):
    current_path = settings.BASE_DIR / 'data' / 'dumps' / str(config.key)
    if not os.path.exists(current_path):
        os.mkdir(current_path)
    return current_path
