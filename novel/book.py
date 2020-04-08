import requests
from bs4.element import Tag
from mechanicalsoup import StatefulBrowser as Browser
from requests.adapters import HTTPAdapter

from . import dav, logger
from .config import DAV_PATH, DB_FILE, HOST, USER_AGENT
from .db import Database


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
                link.append((i+1, (f"{HOST}/thread0806.php?"
                                   f"fid=20&search=&page={i+1}")))
            else:
                link.append((i+1, (f"{HOST}/read.php?"
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
    def __init__(self, url, no=None, pages=None):
        self.no = no
        self.url = url
        self.pages = pages

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
        adapter = HTTPAdapter(max_retries=3)
        requests_adapters = {'http://': adapter, 'https://': adapter}
        browser = Browser(user_agent=USER_AGENT,
                          soup_config={'features': 'html5lib'},
                          requests_adapters=requests_adapters)
        soup = None

        open_exceptions = (
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout
        )
        try:
            browser.open(url, timeout=(5, 60))
        except open_exceptions as e:
            logger.error("url is {}, error is {error}", url, error=e)
            self.__record(url, self.pages)
        except Exception as e:
            logger.error("url is {}, error is {error}", url, error=e)
            self.__record(url, self.pages)
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
            url = HOST + "/" + cleanbg[0].find_all("a")[1]['href']
            return self.__open(url)

    def __record(self, url, pages):
        from urllib.parse import urlparse
        from pathlib import Path

        o = urlparse(url)
        if o.query == "":
            tid = o.path.split('/')[-1][:-5]
        else:
            tid = o.query.split('&')[0][4:]

        pth = Path(__file__).parent / "record.txt"
        with pth.open('a+') as f:
            f.write(f"{tid},{url},{pages}\n")


class Novel(object):
    def __init__(self, url, tid=None, title=None, author=None, date=None,
                 category=None, pages=None):
        """
        url: url for novel first page
        id: id of novel
        title: title of novel
        author: author of novel
        date: create novel blog date
        category: category of novel
        pages: total pages of novel
        """
        self.url = url
        self.id = tid
        self.title = title
        self.author = author
        self.date = date
        self.category = category
        self.pages = pages

        self.content = ''
        self.comment = []
        self.links = []

    def upload(self, dir_path=DAV_PATH):
        db = Database(logger=logger, filename=DB_FILE)
        if db.insert({"id": self.id,
                      "title": self.title,
                      "author": self.author,
                      "date": self.date,
                      "type": self.category,
                      "link": self.url,
                      "size": str(len(self.content)),
                      "page": str(len(self.links))}):
            dav.remove(self.title, self.category, self.id, self.date, dir_path)
            try:
                dav.upload(self.title, self.category, self.id, self.content,
                           self.date, dir_path)
            except OSError as e:
                logger.error("title is {}, error is {err}", self.title, err=e)
            if not dav.exist(self.title, self.category, self.id, self.date,
                             dir_path):
                db.delete(self.id)
        db.close()

    def delete(self):
        db = Database(filename=DB_FILE)
        db.delete(self.id)
        dav.remove(self.title, self.id, self.date)
        db.close()

    def __pagination(self):
        links = [(1, self.url)]
        for i in range(2, self.pages+1):
            links.append((i, (f"{HOST}/read.php?tid={self.id}&page={i}")))
        return links

    def request(self):
        # pagination = Pagination(self.url)
        # self.links = pagination.links
        self.links = self.__pagination()
        for i, link in self.links:
            page = Page(link, i, len(self.links))
            for cell in page.get_cells():
                if cell.author == self.author:
                    self.content += cell.content
                else:
                    self.comment.append((cell.author, cell.content))
