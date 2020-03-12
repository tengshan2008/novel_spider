from context import book, crawel


def book_test():
    url = 'https://cl.330f.tk/htm_data/2002/20/3800260.html'
    tid = '3829529'
    author = 'hohoho12321'
    pages = 5
    novel = book.Novel(url, tid=tid, title='女儿的幸福', date=''
                       category='', author=author, pages=pages)
    novel.request()
    # novel.upload()

    print(novel.author)
    print(novel.content)
    print(novel.links)


def page_test():
    url = 'https://cl.330f.tk/thread0806.php?fid=20&search=&page=1'
    page = crawel.Page(url, 1)
    for i in page.get_items():
        print(i)


if __name__ == "__main__":
    book_test()
    # page_test()
