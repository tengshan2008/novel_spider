import sys
import os
from loguru import logger

base_path = os.path.split(os.path.realpath(__file__))[0]

logger.add(os.path.join(base_path, 'output.log'), encoding='utf-8')

if sys.version_info < (3, 6):
    raise RuntimeError("Only Python 3.6+ is supported.")
