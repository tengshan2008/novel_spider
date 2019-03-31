"""crawel 001banzhu website novels
"""


import random
import time
import os

from robobrowser import RoboBrowser

from banzhu import db, logger
from util import config
import os

base_path = os.path.split(os.path.realpath(__file__))[0]


def run():
    browser = RoboBrowser(parser='html.parser', history=True,
                          timeout=30, tries=5)

    db_file = config.get('sqlite', 'banzhu')
    # dbase = db.get(db_file)

    base_url = config.get('banzhu', 'BaseUrl')
    novel_links = []
    ids_path = os.path.join(base_path, 'ids.txt')
    with open(ids_path, 'r') as f:
        for novel_id in f.readlines():
            novel_links.append(base_url + novel_id)

    for novel_link in novel_links:
        time.sleep(random.randint(2, 5))

        try:
            browser.open(novel_link.strip())
        except Exception as e:
            logger.error('request failed: {}\nerror: {}', novel_link, e)
            continue
        else:
            get_novel(browser, "")

    # db.close(dbase)


def get_novel(browser, dbase):
    logger.info("link {}", browser.url)
    info = browser.find(id='info')
    logger.info(info)
    novel_info = {
        'title': get_title(info),
        'author': get_author(info),
        'last_update': get_last_update(info)
    }

    chapters = browser.find(id='list').find_all('a')
    content = get_content(chapters)
    logger.info(content)
    # if db.insert(novel_info, dbase):
    #     apan.upload(novel_info, content)


def get_title(info):
    return info.find('h1').string


def get_author(info):
    return info.find_all('p')[0].string


def get_last_update(info):
    return info.find_all('p')[2].string


def get_content(chapters):
    browser = RoboBrowser(parser='html.parser', history=True,
                          timeout=30, tries=5)
    content = []
    for chapter in chapters:
        time.sleep(5)

        link = config.get('banzhu', 'BaseUrl') + chapter['href']
        try:
            browser.open(link)
        except:
            logger.error('request failed:', link)
            continue

        content.append('chapter: ' + chapter.string)
        content += get_chapter_content(browser)

    return '\n'.join(content)


def get_chapter_content(browser):
    content = browser.find(id='content')
    if content is None:
        return []
    return [line.strip('\n') for line in content.strings]
