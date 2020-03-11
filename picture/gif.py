from mechanicalsoup import StatefulBrowser as Browser
from pathlib import Path


def get_gif(url):
    with Browser() as browser:
        browser.open(url)
        soup = browser.get_current_page()

    title = soup.head.title.string.strip()
    for i, img in enumerate(soup.body.find_all('img')):
        file_link = img["data-src"]
        file_name = f"{title}_{i}.{file_link.split('.')[-1]}"
        download_link(file_link, file_name)


def download_link(link, filename):
    # pth = Path('/mnt/DAV/images') / filename
    pth = Path('/tmp') / filename
    with Browser() as browser:
        response = browser.open(link)
        with open(pth, 'wb') as f:
            f.write(response.content)
