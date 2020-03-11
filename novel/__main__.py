from . import crawel
from . import book

if __name__ == "__main__":
    url = f"{book.host}/thread0806.php?fid=20&search=&page=1"
    crawl = crawel.Crawl(url)
    crawl.start()
