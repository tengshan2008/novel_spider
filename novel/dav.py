import os
from datetime import datetime
from pathlib import Path

from . import logger
from .config import DAV_PATH

DAV = Path(DAV_PATH)


def get_date_dir(date):
    date_time = datetime.strptime(date, "%Y-%m-%d")
    if date_time.month > 6:
        return f"{date_time.year}下半年合集"
    return f"{date_time.year}上半年合集"


def upload(title, id, date, data):
    dirpath = DAV / get_date_dir(date)
    if not dirpath.exists():
        dirpath.mkdir()
    filepath = dirpath / f"{title}_{id}.txt"
    with filepath.open('w', encoding='utf-8') as f:
        f.write(data)


def remove(title, id, date):
    dirpath = DAV / get_date_dir(date)
    if not dirpath.exists():
        dirpath.mkdir()
    filepath = dirpath / f"{title}_{id}.txt"
    if filepath.exists():
        filepath.unlink()


if __name__ == "__main__":
    result = get_date_dir("2020-02-29")
    print(result)
