import requests
from bs4.element import Tag
from mechanicalsoup import StatefulBrowser as Browser

from .book import Novel, Pagination
from .book import logger, host
from .db import Database


class Page(object):
    def __init__(self, url, no=None):
        self.no = no
        self.url = url

    def get_items(self):
        soup = self.__open(self.url)
        if soup is None:
            return []

        main = soup.body("div", id="main", recursive=False)[0]
        t = main("div", class_="t", recursive=False)[1]
        block_list = t.table.tbody("tr", class_="tr3 t_one tac")
        if self.no == 1:
            block_list = block_list[6:]
        items = []
        for block in block_list:
            item = {}
            link, info, author, _, _ = block("td")
            item["link"] = f"{host}/{link.a['href']}"
            item["type"] = list(info.stripped_strings)[0].strip()
            item["title"] = list(info.stripped_strings)[1].strip()
            if item["type"][0] != "[":
                item["title"] = item["type"]
                item["type"] = "[UNKOWN]"
            if len(list(info.stripped_strings)) > 3:
                item["pages"] = int(list(info.stripped_strings)[-2].strip())
            else:
                item["pages"] = 1
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
        soup = None
        try:
            browser.open(url, timeout=(10, 60))
        except requests.exceptions.ReadTimeout as e:
            logger.error("url is {}, error is {error}", url, error=e)
        except requests.exceptions.ConnectionError as e:
            logger.error("url is {}, error is {error}", url, error=e)
        except Exception as e:
            logger.error("url is {}, error is {error}", url, error=e)
        else:
            soup = browser.get_current_page()
        finally:
            browser.close()
            return soup


class Crawl(object):
    def __init__(self, url):
        self.url = url

    def start(self):
        database = Database(logger=logger, filename='book.db')
        database.init()
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
                              category=item['type'],
                              pages=item['pages'])
                novel.request()
                novel.upload()
