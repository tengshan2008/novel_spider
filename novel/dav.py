import os
from pathlib import Path

from . import logger
from .config import DAV_PATH

DAV = Path(DAV_PATH)


def upload(title, id, data):
    filepath = DAV / f"{title}_{id}.txt"
    filepath.write_text(data, encoding='utf-8')


def remove(title, id):
    filepath = DAV / f"{title}_{id}.txt"
    if filepath.exists():
        filepath.unlink()
