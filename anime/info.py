# from . import book
from mechanicalsoup import StatefulBrowser as Browser
from pathlib import Path
import requests


def get_title(url):
    pass


def get_url(url):
    novel = book.Novel(url)
    novel.request()

    print(novel.content)


# http://www.rmdown.com/download.php
# ?reff=7e4f81ad31908bc9
# &ref=201ec060d86484f402f4e078b585ef023f3264d13ed

# reff=6298cba0d34bf6102b9b930e4f59
# ref=201ec060d86484f402f4e078b585ef023f3264d13ed

# http://www.rmdown.com/download.php
# ?reff=7e4f81ad31908bc9
# &ref=201ec060d86484f402f4e078b585ef023f3264d13ed

# http://www.rmdown.com/download.php?reff=3bf69ea456e07d05&ref=201ec060d86484f402f4e078b585ef023f3264d13ed
# http://www.rmdown.com/download.php?reff=2269ba61404f4&ref=201ec060d86484f402f4e078b585ef023f3264d13ed

def parser(url):
    with Browser() as browser:
        browser.open(url)
        soup = browser.get_current_page()
    form = soup.body.find_all('form')[0]
    params = []
    for param in form.find_all('input'):
        params.append(f"{param['name']}={param['value']}")

    return f"http://www.rmdown.com/download.php?{'&'.join(params)}"


def download_torrent(url, path):
    print(url)
    print(path)
    # with Browser() as browser:
    #     resp = browser.download_link(link=url, file=path)
    # print(resp.status_code)

    response = requests.get(url)
    with open(path, 'wb') as f:
        f.write(response.content)
    print(response.status_code)


def test():
    host = "www.rmdown.com"
    thash = "201ec060d86484f402f4e078b585ef023f3264d13ed"
    url = f"http://{host}/link.php?hash={thash}"
    link = parser(url)
    path = Path(__file__).parent / "test.torrent"
    download_torrent(link, str(path))


if __name__ == "__main__":
    test()

# 1. 打开收藏夹，复制需要下载的网站信息列表
# 2. 粘贴到浏览器中，下载种子文件
