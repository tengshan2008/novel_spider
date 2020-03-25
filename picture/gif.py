from pathlib import Path

import requests
from mechanicalsoup import StatefulBrowser as Browser
from requests.adapters import HTTPAdapter

from . import db, logger
from .config import IMAGES_PATH, USER_AGENT, DB_FILE

open_exceptions = (
    requests.exceptions.ReadTimeout,
    requests.exceptions.ConnectionError,
    requests.exceptions.ConnectTimeout
)


class Page(object):
    def __init__(self, url=None):
        self.url = url

    def parse(self):
        soup = None
        with Browser() as browser:
            try:
                browser.open(self.url, timeout=(10, 30))
            except open_exceptions as e:
                logger.error("url is {}, error is {error}", self.url, error=e)
            except Exception as e:
                logger.error("url is {}, error is {error}", self.url, error=e)
            else:
                soup = browser.get_current_page()
        if soup is None:
            logger.error("parse {} failed.", self.url)
            return None
        self.soup = soup

        self.imgs = self.soup.body.find_all('img')
        self.title = self.soup.head.title.string.strip()
        self.filter_title()
        self.get_title()

    def get_title(self):
        tid = self.url.split('/')[-1][:-5]
        title = self.title.replace("技術討論區草榴社區", "")
        self.title = f"{title}_[{len(self.imgs)}P]_{tid}"

    def filter_title(self):
        # Invaild symbol \ / : * ? < > |
        title = self.title
        title = title.replace("\\", '')
        title = title.replace('/', '')
        title = title.replace(':', '：')
        title = title.replace('*', '')
        title = title.replace('?', '？')
        title = title.replace('<', '《')
        title = title.replace('>', '》')
        title = title.replace('|', '')
        title = title.replace('(', '（')
        title = title.replace(')', '）')
        title = title.replace(' ', '')
        self.title = title

    def download_link(self, dirpath, link, filename):
        pth = Path(dirpath) / filename
        if pth.exists():
            return None

        database = db.Database(DB_FILE)

        adapter = HTTPAdapter(max_retries=3)
        requests_adapters = {'http://': adapter, 'https://': adapter}

        with Browser(user_agent=USER_AGENT,
                     requests_adapters=requests_adapters) as browser:
            try:
                response = browser.open(link, timeout=(120, 120))
            except open_exceptions as e:
                logger.error("url is {}, error is {error}", link, error=e)
                database.insert(self.title, link, filename)
            except Exception as e:
                logger.error("url is {}, error is {error}", link, error=e)
                database.insert(self.title, link, filename)
            else:
                if pth.exists():
                    pth.unlink()
                with pth.open('wb') as f:
                    f.write(response.content)
                logger.info("{title} {filename} finished",
                            title=self.title, filename=filename)

    def download(self, dir_path=IMAGES_PATH):
        dirpath = Path(dir_path) / self.title
        if not dirpath.exists():
            dirpath.mkdir()

        html = dirpath / f"{self.title}.html"
        html.write_text(str(self.soup))

        for i, img in enumerate(self.imgs):
            file_link = ""
            if "data-src" in img.attrs:
                file_link = img["data-src"]
            if "data-ssa" in img.attrs:
                file_link = img["data-ssa"]
            if file_link == "":
                logger.warning("{img} not found url", img=img)
                continue
            ext = file_link.split('.')[-1]
            if len(ext) > 7:
                continue
            file_name = f"{i+1}.{ext}"
            self.download_link(str(dirpath), file_link, file_name)
