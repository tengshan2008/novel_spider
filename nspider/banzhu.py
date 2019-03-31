from robobrowser import RoboBrowser
from loguru import logger

import time

from nspider import db, config, apan


def run(url):
    browser = RoboBrowser(parser='html.parser', history=True,
                          timeout=30, tries=5)

    db_file = config.get('sqlite', 'banzhu')
    dbase = db.get(db_file)

    ids = []
    with open(ids_path, 'r') as f:
        ids = f.readlines()

    for novel_id in ids:
        novel_link = config.get('banzhu', 'BaseUrl') + novel_id
        logger.info('link ', novel_link)
        time.sleep(5)

        try:
            browser.open(novel_link.strip())
        except:
            logger.error('request error', novel_link)
            continue
        else:
            get_novel(browser, novel_id, dbase)

    db.close(dbase)


def get_novel(browser, novel_id, dbase):
    info = browser.find(id='info')
    novel_info = {
        'title': get_title(info),
        'author': get_author(info),
        'last_update': get_last_update(info)
    }

    chapters = browser.find(id='list').find_all('a')
    content = get_content(chapters)
    if db.insert(novel_info, dbase):
        apan.upload(novel_info, content)


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

