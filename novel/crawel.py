import requests
from bs4.element import Tag
from mechanicalsoup import StatefulBrowser as Browser

from book import Novel, Pagination, logger
from db import Database

host = "https://cl.330f.tk"


class Page(object):
    def __init__(self, url, no=None):
        self.no = no
        self.url = url

    def get_items(self):
        soup = self.__open(self.url)
        main = soup.body("div", id="main", recursive=False)[0]
        t = main("div", class_="t", recursive=False)[1]
        block_list = t.table.tbody("tr", class_="tr3 t_one tac")[6:]
        items = []
        for block in block_list:
            item = {}
            link, title, author, _, _ = block("td")
            item["link"] = f"{host}/{link.a['href']}"
            type_title = [i.strip() for i in list(title.strings)[:2]]
            item["type"], item["title"] = type_title
            item["author"] = author.a.string.strip()
            if author.div.span is None:
                item["date"] = author.div.string.strip()
            else:
                item["date"] = author.div.span.string.strip()
            item["id"] = item["link"].split('/')[-1][:-5]
            items.append(item)
        return items

    def __open(self, url):
        browser = Browser()
        try:
            browser.open(url, timeout=(5, 60))
        except requests.exceptions.ReadTimeout as e:
            logger.error("url is {}, error is {error}", url, error=e)
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error("url is {}, error is {error}", url, error=e)
            return None
        else:
            soup = browser.get_current_page()
            return soup


class Crawl(object):
    def __init__(self, url):
        self.url = url

    def start(self):
        db = Database(logger=logger, filename='book.db')
        db.init()
        self.__request_novel_list()

    def __request_novel_list(self):
        pagination = Pagination(self.url, page_type="out")
        for i, link in pagination.links:
            page = Page(link, i)
            for item in page.get_items():
                novel = Novel(url=item['link'],
                              tid=item['id'],
                              title=item['title'],
                              author=item['author'],
                              date=item['date'],
                              category=item['type'])
                novel.request()
                novel.upload()


if __name__ == "__main__":
    # crawl = Crawl('https://cl.330f.tk/thread0806.php?fid=20&search=&page=1')
    # crawl.start()
    page = Page('https://cl.330f.tk/thread0806.php?fid=20&search=&page=1', 1)
    for i in page.get_items():
        print(i)
