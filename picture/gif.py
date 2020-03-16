from pathlib import Path

import requests
from mechanicalsoup import StatefulBrowser as Browser
from requests.adapters import HTTPAdapter

from . import logger

USER_AGENT = """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/\
537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"""

IMAGES_PATH = "/media/share/other/images"

open_exceptions = (
    requests.exceptions.ReadTimeout,
    requests.exceptions.ConnectionError,
    requests.exceptions.ConnectTimeout
)


class Page(object):
    def __init__(self, url):
        self.url = url
        self.init()

    def init(self):
        with Browser() as browser:
            try:
                browser.open(self.url, timeout=(10, 30))
            except open_exceptions as e:
                logger.error("url is {}, error is {error}", self.url, error=e)
            except Exception as e:
                logger.error("url is {}, error is {error}", self.url, error=e)
            else:
                soup = browser.get_current_page()

        self.imgs = soup.body.find_all('img')
        self.title = soup.head.title.string.strip()
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

    def download_link(self, dir_path, link, filename):
        dirpath = Path(dir_path) / self.title
        if not dirpath.exists():
            dirpath.mkdir()
        pth = dirpath / filename
        if pth.exists():
            return None

        adapter = HTTPAdapter(max_retries=3)
        requests_adapters = {'http://': adapter, 'https://': adapter}

        with Browser(user_agent=USER_AGENT,
                     requests_adapters=requests_adapters) as browser:
            try:
                response = browser.open(link, timeout=(90, 90))
            except open_exceptions as e:
                logger.error("url is {}, error is {error}", link, error=e)
            except Exception as e:
                logger.error("url is {}, error is {error}", link, error=e)
            else:
                if pth.exists():
                    pth.unlink()
                with pth.open('wb') as f:
                    f.write(response.content)
                logger.info("{title} {filename} finished",
                            title=self.title, filename=filename)

    def download(self, dir_path=IMAGES_PATH):
        for i, img in enumerate(self.imgs):
            file_link = img["data-src"]
            file_name = f"{i+1}.{file_link.split('.')[-1]}"
            self.download_link(dir_path, file_link, file_name)
