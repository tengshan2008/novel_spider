import os
import re
import time

import requests
from bs4.element import Tag
from loguru import logger
from mechanicalsoup import StatefulBrowser as Browser

import dav
from db import Database

base_path = os.path.split(os.path.realpath(__file__))[0]

logger.add(os.path.join(base_path, 'output.log'),
           colorize=True, encoding='utf-8')

host = "https://cl.330f.tk"

USER_AGENT = """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/\
537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"""


class Pagination(object):
    def __init__(self, url, page_type=None):
        self.page_type = page_type
        self.links = self.__parse(url)

    def __open(self, url):
        browser = Browser(user_agent=USER_AGENT)
        soup = None
        try:
            browser.open(url, timeout=(10, 60))
        except requests.exceptions.ReadTimeout as e:
            logger.error("url is {}, error is {error}", url, error=e)
        except requests.exceptions.ConnectionError as e:
            logger.error("url is {}, error is {error}", url, error=e)
        except requests.exceptions.SSLError as e:
            logger.error("url is {}, error is {error}", url, error=e)
        except Exception as e:
            logger.error("url is {}, error is {error}", url, error=e)
        else:
            soup = browser.get_current_page()
        finally:
            browser.close()
            return soup

    def __parse(self, url):
        soup = self.__open(url)
        if soup is None:
            return []

        pages = soup.find_all("div", class_="pages")
        if len(pages) == 0:
            return [(1, url)]

        w70 = pages[0].find_all("a", class_="w70")
        if len(w70) == 0:
            return [(1, url)]

        last_link = w70[0]
        value = last_link.input.attrs['value']
        onkeydown = last_link.input.attrs['onkeydown']
        tid = onkeydown.split('?')[1].split('&')[0][4:]
        last = int(value.split('/')[1])

        link = [(1, url)]
        for i in range(1, last):
            if self.page_type == "out":
                link.append((i+1, (f"{host}/thread0806.php?"
                                   f"fid=20&search=&page={i+1}")))
            else:
                link.append((i+1, (f"{host}/read.php?"
                                   f"tid={tid}&page={i+1}")))
        return link


class Cell(object):
    def __init__(self, data: Tag):
        self.author, self.date, self.level, self.content = self.__parse(data)

    def __parse(self, data: Tag):
        chead = data.table.tr.th
        cbody = data.tr("th", recursive=False)[1]
        cfoot = data.table.tbody("tr", recursive=False)[1]
        author = self.__get_author(chead)
        date, level = self.__get_date_level(cfoot)
        content = self.__get_content(cbody)
        return author, date, level, content

    def __get_author(self, data: Tag):
        return next(data.b.strings).strip()

    def __get_date_level(self, data: Tag):
        _, posted, floor = list(data.th("div",
                                        class_="tipad",
                                        recursive=False)[0].stripped_strings)
        return posted[7:23], floor

    def __get_content(self, data: Tag):
        div = data("div", class_="tpc_content")[0]
        return '\n'.join(list(div.stripped_strings))


class Page(object):
    def __init__(self, url, no=None):
        self.no = no
        self.url = url

    def get_cells(self):
        soup = self.__open(self.url)
        if soup is None:
            return []
        main = soup.body("div", id="main", recursive=False)[0]
        if len(main("form")) > 0 and main.form["name"] == "delatc":
            main = main.form
        for t_t2 in main("div", class_="t t2", recursive=False):
            yield Cell(t_t2)

    def __open(self, url):
        browser = Browser(user_agent=USER_AGENT,
                          soup_config={'features': 'html5lib'})
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
            soup = self.redirect(soup)
        finally:
            browser.close()
            return soup

    def redirect(self, data: Tag):
        cleanbg = data.find_all("div", class_="cleanbg")
        if len(cleanbg) == 0:
            return data
        else:
            url = host + "/" + cleanbg[0].find_all("a")[1]['href']
            return self.__open(url)


class Novel(object):
    def __init__(self, url, tid=None, title=None, author=None, date=None,
                 category=None, pages=None):
        """
        url: url for novel first page
        """
        self.url = url
        self.id = tid
        self.title = title
        self.author = author
        self.date = date
        self.category = category
        self.pages = pages
        self.content = ''
        self.links = []

    def upload(self):
        db = Database(logger=logger, filename='book.db')
        if db.insert({"id": self.id,
                      "title": self.title,
                      "author": self.author,
                      "date": self.date,
                      "type": self.category,
                      "link": self.url,
                      "size": str(len(self.content)),
                      "page": str(len(self.links))}):
            dav.upload(self.title, self.id, self.content)
        db.close()

    def delete(self):
        db = Database(filename='book.db')
        db.delete(self.id)
        dav.remove(self.title, self.id)
        db.close()

    def __pagination(self):
        links = [(1, self.url)]
        for i in range(2, self.pages+1):
            links.append((i, (f"{host}/read.php?tid={self.id}&page={i}")))
        return links

    def request(self):
        # pagination = Pagination(self.url)
        # self.links = pagination.links
        self.links = self.__pagination()
        for i, link in self.links:
            page = Page(link, i)
            for cell in page.get_cells():
                if cell.author == self.author:
                    self.content += cell.content


if __name__ == "__main__":
    url = 'https://cl.330f.tk/htm_data/2002/20/3829529.html'
    author = '路易十三'
    pages = 4
    novel = Novel(url, tid='3829529', title='未知', author=author, pages=pages)
    novel.request()
    # novel.upload()

    print(novel.author)
    print(novel.content)
    print(novel.links)
    # page = Page(url, 1)
    # for cell in page.get_cells():
    #     print(cell.author)
    #     print(cell.content)
