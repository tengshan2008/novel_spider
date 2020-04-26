from context import book, fix, crawel


def book_test():
    info = {
        "id": 1091271,
        "title": "雪域往事[五部共105章结]",
        "author": "武当山",
        "date": "2014-05-25",
        "type": "[現代奇幻]",
        "link": "https://cb.321i.xyz/htm_data/1405/20/1091271.html",
        "pages": 44
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
