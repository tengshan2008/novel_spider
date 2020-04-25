from context import book, fix, crawel


def book_test():
    info = {
        "id": 1100313,
        "title": "金海陵纵欲亡身（更新完）",
        "author": "茎滑水跃",
        "date": "2014-05-08",
        "type": "[古典武俠]",
        "link": "https://cb.321i.xyz/htm_data/1405/20/1100313.html",
        "pages": 11
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
