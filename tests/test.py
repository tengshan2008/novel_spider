from context import book, crawel


def book_test():
    url = 'https://cl.330f.tk/htm_data/2002/20/3829529.html'
    author = '路易十三'
    pages = 4
    novel = book.Novel(url, tid='3829529', title='未知',
                       author=author, pages=pages)
    novel.request()

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
