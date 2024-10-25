import argparse

from loguru import logger

from app.settings import Settings
from managers.config_manager import ConfigManager
from managers.dump_manager import DumpManager


def main():
    parser = argparse.ArgumentParser(description='Init app')
    parser.add_argument('--name', type=str, help='Config name')
    args = parser.parse_args()

    settings = Settings()
    logger.info({'event': 'START_APP', 'debug': settings.debug})

    name = args.name
    config = ConfigManager().get_config_by_name(name)
    if not config:
        logger.warning({'event': 'FIND_CONFIG', 'error': f'Config "{name}" not found.'})
        return
    DumpManager(config).process()


if __name__ == '__main__':
    main()
