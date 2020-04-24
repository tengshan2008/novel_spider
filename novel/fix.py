from pathlib import Path

from loguru import logger

from .book import Novel, Page
from .config import DB_FILE
from .db import Database

record_path = Path(__file__).parent / 'record-need.txt'


def load_record():
    items = {}
    with record_path.open('r') as f:
        for line in f.readlines():
            tid, url, pages = line.strip().split(',')
            tid_pages = tid + "_" + pages
            if tid_pages in items:
                items[tid_pages].append(url)
            else:
                items[tid_pages] = [url]
    return items


def remove_record():
    if record_path.exists():
        record_path.unlink()
    else:
        print('record file not exst')


def get_novel_info(tid):
    db = Database(logger, DB_FILE)
    return db.read(tid)


def reload_novel(info, pages):
    novel = Novel(url=info['link'],
                  tid=info['id'],
                  title=info['title'],
                  author=info['author'],
                  date=info['date'],
                  category=info['type'],
                  pages=pages)
    novel.request()
    novel.upload()


def main():
    for tid_pages, urls in load_record().items():
        tid, pages = tid_pages.split('_')
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
            reload_novel(info, pages)
