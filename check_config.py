from loguru import logger

from app.settings import Settings
from managers.config_manager import ConfigManager


def main():
    settings = Settings()
    ConfigManager()
    logger.info({'event': 'CHECK_CONFIG', 'ok': True, 'debug': settings.debug})


if __name__ == '__main__':
    main()
