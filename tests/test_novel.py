from context import book, fix, crawel


def book_test():
    info = {
        "id": 3823103,
        "title": "火车上的女孩儿",
        "author": "潇湘竹",
        "date": "2020-02-23",
        "type": "[現代奇幻]",
        "link": "https://cl.dn37.xyz/htm_data/2002/20/3823103.html",
        "pages": 7
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
