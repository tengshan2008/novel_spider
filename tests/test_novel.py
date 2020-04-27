from context import book, fix, crawel
import time
from pathlib import Path


def book_test():
    info = {
        "id": 1143113,
        "title": "会所男公关：官太太（1-168）[全本完]",
        "author": "38℃",
        "date": "2014-07-25",
        "type": "[現代奇幻]",
        "link": "https://cb.321i.xyz/htm_data/1407/20/1143113.html",
        "pages": 77
    }
    novel = book.Novel(info['link'], tid=str(info['id']), title=info['title'],
                       date=info['date'], category=info['type'],
                       author=info['author'], pages=info['pages'])
    novel.request()
    # dir_path = "/tmp"
    novel.upload()
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
