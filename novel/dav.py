import os
from pathlib import Path

DAV = Path('/mnt/DAV/book')


def upload(title, id, data):
    filepath = DAV / f"{title}_{id}.txt"
    filepath.write_text(data, encoding='utf-8')


def remove(title, id):
    filepath = DAV / f"{title}_{id}.txt"
    if filepath.exists():
        filepath.unlink()
    else:
        print('file not exist')


if __name__ == "__main__":
    upload('test', 'ab12', 'this is a test/nbbb')
    remove('test', 'ab12')
