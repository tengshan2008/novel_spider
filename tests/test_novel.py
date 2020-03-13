from context import book, check, crawel


def book_test():
    url = 'https://cl.330f.tk/htm_data/2003/5/3845387.html'
    tid = '3845387'
    author = '大神魔'
    pages = 1
    novel = book.Novel(url, tid=tid, title="「(原创)3D SuMthinDiFrnt - Man's Best Friend 2」.无码/MP4/1.6GB", date='',
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


def check_test():
    tid = '3842268'
    result = check.get_novel_info(tid)
    print(result)


if __name__ == "__main__":
    book_test()
    # page_test()
    # check_test()
