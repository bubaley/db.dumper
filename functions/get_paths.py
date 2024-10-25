import os
import secrets
from datetime import datetime
from pathlib import Path

from managers.config_manager import Config, ConfigManager


def get_dump_filename():
    date = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f'dump_{date}_{secrets.token_hex(nbytes=2)}.sql'


def get_config_dump_folder_path(config: Config):
    dumps_folder_path = ConfigManager.get_dumps_folder_path()
    current_path = Path(dumps_folder_path, config.settings.name)
    if not os.path.exists(current_path):
        os.mkdir(current_path)
    return str(current_path)
