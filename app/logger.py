import sys

from loguru import logger

logger.remove()

format_values = [
    '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>',
    '<level>{level: <8}</level>',
    '{message}',
    '<cyan>{file.name}<red>:</red>{function}<red>:</red>{line}</cyan>',
]

logger.add(
    sys.stdout,
    format=' <red>|</red> '.join(format_values),
)
