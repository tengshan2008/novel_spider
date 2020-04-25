from context import book, fix, crawel


def book_test():
    info = {
        "id": 999317,
        "title": "百花仙子（全文完）",
        "author": "夏沫花谢",
        "date": "2013-12-29",
        "type": "[現代奇幻]",
        "link": "https://cb.321i.xyz/htm_data/1312/20/999317.html",
        "pages": 27
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
