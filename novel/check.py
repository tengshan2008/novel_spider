from pathlib import Path
from .book import Novel

record_path = Path(__file__).parent / 'record.txt'


def load_record():
    with record_path.open('r') as f:
        return [url.strip() for url in f.readlines()]


def remove_record():
    if record_path.exists():
        record_path.unlink()
    else:
        print('record file not exst')


def main():
    urls = load_record()
    for url in load_record():
        novel = Novel(url)
        novel.request()
        novel.upload()
