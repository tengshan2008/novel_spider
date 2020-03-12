from pathlib import Path

from . import logger, DB_FILE
from .book import Page, Novel
from .db import Database

record_path = Path(__file__).parent / 'record.txt'


def load_record():
    items = {}
    with record_path.open('r') as f:
        for line in f.readlines():
            tid, url = line.strip().split(',')
            if tid in items:
                items[tid].append(url)
            else:
                items[tid] = [url]
    return items


def remove_record():
    if record_path.exists():
        record_path.unlink()
    else:
        print('record file not exst')


def get_novel_info(tid):
    db = Database(logger, DB_FILE)


def reload_novel(info):
    novel = Novel(url=info['link'],
                  tid=info['id'],
                  title=info['title'],
                  author=info['author'],
                  date=info['date'],
                  category=info['type'],
                  pages=info['pages'])
    novel.request()
    novel.upload()


def main():
    for tid, urls in load_record().items():
        info = get_novel_info(tid)
        need_reload = False
        for url in urls:
            page = Page(url)
            for cell in page.get_cells():
                if cell.author == info["author"]:
                    need_reload = True
                    break
            if reload_novel:
                break
        if need_reload:
            reload_novel(info)
