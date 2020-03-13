from pathlib import Path

import requests
from mechanicalsoup import StatefulBrowser as Browser
from requests.adapters import HTTPAdapter

from . import logger

USER_AGENT = """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/\
537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"""

open_exceptions = (
    requests.exceptions.ReadTimeout,
    requests.exceptions.ConnectionError,
    requests.exceptions.ConnectTimeout
)


def filter_title(title):
    # Invaild symbol \ / : * ? < > |
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
    return title


def get_gif(url):
    with Browser() as browser:
        try:
            browser.open(url, timeout=(10, 30))
        except open_exceptions as e:
            logger.error("url is {}, error is {error}", url, error=e)
        except Exception as e:
            logger.error("url is {}, error is {error}", url, error=e)
        else:
            soup = browser.get_current_page()

    title = filter_title(soup.head.title.string.strip())
    for i, img in enumerate(soup.body.find_all('img')):
        file_link = img["data-src"]
        file_name = f"{i+1}.{file_link.split('.')[-1]}"
        download_link(file_link, title, file_name)


def download_link(link, dirname, filename):
    dirpath = Path('/mnt/DAV/images') / dirname
    if not dirpath.exists():
        dirpath.mkdir()
    pth = dirpath / filename

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
            logger.info("{title} finished", title=filename)
