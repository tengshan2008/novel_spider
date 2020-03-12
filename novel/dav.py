import os
from pathlib import Path

from . import logger
from .config import DAV_PATH

DAV = Path(DAV_PATH)


def upload(title, id, data):
    filepath = DAV / f"{title}_{id}.txt"
    with filepath.open('w', encoding='utf-8') as f:
        f.write(data)


def remove(title, id):
    filepath = DAV / f"{title}_{id}.txt"
    if filepath.exists():
        filepath.unlink()
