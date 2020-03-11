import requests
from bs4.element import Tag
from mechanicalsoup import StatefulBrowser as Browser

from . import logger
from .book import Novel, Pagination
from .config import DB_FILE, HOST
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
            item["link"] = self.__get_link(link)
            item["title"], item["type"] = self.__get_title_type(info)
            item["pages"] = self.__get_pages(info)
            item["author"] = self.__get_author(author)
            item["date"] = self.__get_date(author)
            item["id"] = self.__get_id(item["link"])
            items.append(item)
        return items

    def __get_link(self, data):
        return f"{HOST}/{data.a['href']}"

    def __get_title_type(self, data):
        novel_title = list(data.stripped_strings)[1].strip()
        novel_type = list(data.stripped_strings)[0].strip()
        if novel_type[0] != "[":
            novel_title = novel_type
            novel_type = "[UNKOWN]"
        return self.__filter_title(novel_title), novel_type

    def __get_pages(self, data):
        if len(list(data.stripped_strings)) > 3:
            return int(list(data.stripped_strings)[-2].strip())
        return 1

    def __get_author(self, data):
        return data.a.string.strip()

    def __get_date(self, data):
        if data.div.span is None:
            return data.div.string.strip()
        return data.div.span.string.strip()

    def __get_id(self, data):
        return data.split('/')[-1][:-5]

    def __filter_title(self, title):
        title = title.replace(':', '：')
        title = title.replace('(', "（")
        title = title.replace(')', "）")
        return title

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
    def __init__(self, url, start_page):
        self.url = url
        self.start_page = start_page

    def start(self):
        database = Database(logger=logger, filename=DB_FILE)
        database.init()
        self.__request_novel_list()

    def __request_novel_list(self):
        pagination = Pagination(self.url, page_type="out")
        for i, link in pagination.links[self.start_page-1:]:
            logger.info("start crawl page {}", i)
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
