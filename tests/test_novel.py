from context import book, fix, crawel


def book_test():
    url = 'https://cl.330f.tk/htm_data/2003/5/3845387.html'
    tid = '3845387'
    author = '大神魔'
    pages = 1
    title = "「(原创)3D SuMthinDiFrnt - Man's Best Friend 2」.无码MP41.6GB"
    date = '2020-3-16'
    novel = book.Novel(url, tid=tid, title=title, date=date,
                       category='', author=author, pages=pages)
    novel.request()
    novel.upload(dir_path="/tmp")
    print(novel.author)
    print(novel.content)
    print(novel.links)


def page_test():
    url = 'https://cl.330f.tk/thread0806.php?fid=20&search=&page=9'
    page = crawel.Page(url, 9)
    for i in page.get_items():
        print(i)


def fix_test():
    tid = '3842268'
    result = fix.get_novel_info(tid)
    print(result)


def fix_load_test():
    for k, v in fix.load_record().items():
        print(k, v)


if __name__ == "__main__":
    # book_test()
    # page_test()
    # fix_test()
    fix_load_test()
