from context import book, fix, crawel


def book_test():
    info = {
        "id": 1282154,
        "title": "[先鋒原創文學]殞落城市（全）",
        "author": "曉秋",
        "date": "2014-12-18",
        "type": "[另類禁忌]",
        "link": "https://cb.321i.xyz/htm_data/1412/20/1282154.html",
        "pages": 16
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


def fix_load_test():
    fix.main()


if __name__ == "__main__":
    book_test()
    # page_test()
    # fix_test()
    # fix_load_test()
    # temp()
