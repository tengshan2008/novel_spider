from pathlib import Path

from loguru import logger

from . import book, crawel

logger.add(Path(__file__).parent / 'output.log',
           colorize=True, encoding='utf-8')

host = "https://cl.330f.tk"
