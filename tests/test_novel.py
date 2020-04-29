import time
from pathlib import Path

import requests

from context import book, crawel, fix

SCKEY = "SCU94031T56e85df7072dc2c313d2f4de1b3ef1315e96c7a1afe53"


def book_test():
    info = {'link': 'https://cl.hn32.xyz/htm_data/1911/20/3705515.html', 'title': '淫母计划1-7', 'type': '[另類禁忌]', 'pages': 12, 'author': '晨起凸起', 'date': '2019-11-07', 'id': 3705515}
    novel = book.Novel(info['link'], tid=str(info['id']), title=info['title'],
                       date=info['date'], category=info['type'],
                       author=info['author'], pages=info['pages'])
    novel.request()
    # dir_path = "/tmp"
    novel.upload()
    payload = {'text': f"script finished, id is {info['id']}",
               'desp': f"title is {info['title']}"}
    requests.get(url=f"https://sc.ftqq.com/{SCKEY}.send", params=payload)
    # print(novel.author)
    # print(novel.content)
    # print(novel.links)


def page_test():
    url = 'https://cl.330f.tk/thread0806.php?fid=20&search=&page=9'
    page = crawel.Page(url, 9)
    for i in page.get_items():
        print(i)


def info_cache():
    items = []
    for i in range(1, 27):
        time.sleep(10)
        url = f"https://cl.hn32.xyz/thread0806.php?fid=20&search=&page={i}"
        page = crawel.Page(url, i)
        for item in page.get_items():
            items.append(str(item))
    with open('tests/novel_info.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(items))


def local_cache():
    book_names = []
    books = Path("/mnt/DAV/teracloud/Books")
    for year in books.iterdir():
        if year.is_dir():
            for book in year.iterdir():
                if '.txt' in str(book):
                    book_names.append(book.stem)
    with open('tests/local_info.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(book_names))


def fix_load_test():
    fix.main()


def diff_load():
    # lines = []
    with open('tests/novel_cache.txt', 'r', encoding='utf-8') as f:
        lines = [int(eval(line.strip())['id']) for line in f.readlines()]
    lines.sort()
    with open('/tmp/online_tid.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join([str(line) for line in lines]))


if __name__ == "__main__":
    book_test()
    # page_test()
    # fix_test()
    # fix_load_test()
    # temp()
    # info_cache()
    # local_cache()
    # diff_load()
