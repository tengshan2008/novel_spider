from context import book, fix, crawel


def book_test():
    info = {
        "id": 1016265,
        "title": "夜幕下的恶魔（已完结）",
        "author": "dasfdafd",
        "date": "2014-01-13",
        "type": "[現代奇幻]",
        "link": "https://cb.321i.xyz/htm_data/1401/20/1016265.html",
        "pages": 13
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
