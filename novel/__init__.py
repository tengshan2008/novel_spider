from pathlib import Path

from loguru import logger

from . import book, crawel, fix

logger.add(Path(__file__).parent / 'output.log',
           colorize=True, encoding='utf-8')
