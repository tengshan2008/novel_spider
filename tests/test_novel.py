from context import book, fix, crawel


def book_test():
    url = 'https://cl.dn37.xyz/htm_data/2002/20/3825331.html'
    tid = '3825331'
    author = '小黄文'
    pages = 4
    title = "[原创]毕业生"
    date = '2020-02-24'
    category = '[現代奇幻]'
    novel = book.Novel(url, tid=tid, title=title, date=date,
                       category=category, author=author, pages=pages)
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
