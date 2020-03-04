import re
import time
import os

from bs4.element import Tag
from mechanicalsoup import StatefulBrowser as Browser

import dav
from db import Database
from loguru import logger

base_path = os.path.split(os.path.realpath(__file__))[0]

logger.add(os.path.join(base_path, 'output.log'),
           colorize=True, encoding='utf-8')

host = "https://cl.330f.tk"


class Pagination(object):
    def __init__(self, url, page_type=None):
        self.page_type = page_type
        self.links = self.__parse(url)

    def __parse(self, url):
        browser = Browser()
        print(url)
        browser.open(url)
        soup = browser.get_current_page()

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

        link = []
        for i in range(last):
            if self.page_type == "out":
                link.append((i+1, f"{host}/thread0806.php?fid=20&search=&page={i+1}"))
            else:
                link.append((i+1, f"{host}/read.php?tid={tid}&page={i+1}"))
        return link


class Cell(object):
    def __init__(self, data: Tag):
        self.author, self.date, self.level, self.content = self.__parse(data)

    def __parse(self, data: Tag):
        chead = data.table.tr.th
        cbody = data.tr("th", recursive=False)[1]
        cfoot = data.table("tr", recursive=False)[1]
        author = self.__get_author(chead)
        date, level = self.__get_date_level(cfoot)
        content = self.__get_content(cbody)
        return author, date, level, content

    def __get_author(self, data: Tag):
        return data.b.string

    def __get_date_level(self, data: Tag):
        _, posted, floor = list(data.th("div",
                                        class_="tipad",
                                        recursive=False)[0].stripped_strings)
        return posted[7:23], floor

    def __get_content(self, data: Tag):
        # div = data.table.tr.td("div",
        #                        class_="tpc_content",
        #                        recursive=False)[0]
        div = data("div", class_="tpc_content")[0]
        return '\n'.join(list(div.stripped_strings))


class Page(object):
    def __init__(self, url, no=None):
        self.no = no
        self.url = url

    def get_cells(self):
        soup = self.__open(self.url)
        main = soup.body("div", id="main", recursive=False)[0]
        if main.form["name"] == "delatc":
            main = main.form
        for t_t2 in main("div", class_="t t2", recursive=False):
            yield Cell(t_t2)

    def __open(self, url):
        browser = Browser()
        print(url)
        browser.open(url)
        soup = browser.get_current_page()
        soup = self.redirect(soup)
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
                 category=None):
        """
        url: url for novel first page
        """
        self.url = url
        self.id = tid
        self.title = title
        self.author = author
        self.date = date
        self.category = category
        self.content = ''
        self.links = []

    def upload(self):
        db = Database(logger=logger, filename='book.db')
        db.init()
        if db.insert({"id": self.id,
                      "title": self.title,
                      "author": self.author,
                      "date": self.date,
                      "type": self.category,
                      "link": ':'.join(self.links),
                      "size": str(len(self.content)),
                      "page": str(len(self.links))}):
            dav.upload(self.title, self.id, self.content)

    def delete(self):
        db = Database(filename='book.db')
        db.delete(self.id)
        dav.remove(self.title, self.id)

    def __parse_page(self, url):
        if self.id == "":
            self.__get_id(url)
        if self.title == "":
            self.__get_title(url)
        if self.author == "":
            self.__get_author(url)
        if self.date == "":
            self.__get_date(url)
        if self.category == "":
            self.__get_category(url)

    def __get_id(self, url):
        pass

    def __get_title(self, url):
        pass

    def __get_author(self, url):
        pass

    def __get_date(self, url):
        pass

    def __get_category(self, url):
        pass

    def __get_cells(self, url):
        pass

    def request(self):
        pagination = Pagination(self.url)
        self.links = pagination.links
        for i, link in pagination.links:
            page = Page(link, i)
            for cell in page.get_cells():
                if cell.author == self.author:
                    self.content += cell.content


if __name__ == "__main__":
    # url, author = 'https://cb.386i.xyz/htm_data/2001/20/3778625.html', '晨起凸起'
    # url = 'https://cb.386i.xyz/read.php?tid=3777610&page=2'
    # url = 'https://cb.386i.xyz/htm_data/2001/20/3779065.html'
    # url = 'https://cb.386i.xyz/htm_data/2001/20/3777760.html'
    # author = 'yq8226171'
    # url = 'https://cb.386i.xyz/htm_data/2001/20/3768299.html'
    url = 'https://cl.330f.tk/htm_data/2002/20/3828496.html'
    author = '潇湘竹'
    # url = 'https://cb.386i.xyz/htm_data/0803/20/118995.html'
    # author = 'ROLLIN'
    novel = Novel(url, tid='ab12', title='未知', author=author)

    novel.request()

    # dav.upload(novel.title, novel.id, novel.content)
    print(novel.author)
    print(novel.content)
    print(novel.links)
    # page = Page(url, 1)
    # for cell in page.get_cells():
    #     print(cell.author)
    #     print(cell.content)
