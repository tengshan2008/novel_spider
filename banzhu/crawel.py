"""crawel 001banzhu website novels
"""

import datetime
import os
import random
import re
import time
import string

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from robobrowser import RoboBrowser

from banzhu import db, logger
from pipline import apan
from util import config

base_path = os.path.split(os.path.realpath(__file__))[0]


def run(url: str):
    browser = RoboBrowser(parser='html5lib', history=True,
                          timeout=30, tries=5, multiplier=0.3)

    try:
        browser.open(url)
    except (requests.exceptions.Timeout, requests.ConnectionError) as e:
        logger.error('request fail {url}, {err}', url=url, err=e)
        return
    except:
        logger.exception('request failed: {url}', url=url)

    db_file = config.get('sqlite', 'banzhu')
    dbase = db.get(db_file)

    count = 1
    while True:
        logger.info("current page is {}", count)
        for novel in get_novels(browser):
            time.sleep(random.randint(2, 5))
            novel_info = get_novel_info(novel)
            novel_content = get_novel_content(novel_info)
            novel_info['size'] = str(len(novel_content))
            if db.insert(novel_info, dbase):
                ok = apan.upload(novel_info, novel_content)
                if not ok:
                    db.delete(novel_info, dbase)
        if is_end_page(browser):
            break
        try:
            browser.follow_link(next_page(browser))
        except (requests.exceptions.Timeout, requests.ConnectionError) as e:
            logger.error()
            db.close(dbase)
            return
        except:
            logger.exception('request failed: {url}', url=browser.url)
            db.close(dbase)
            return
        count += 1
    
    db.close(dbase)

def is_end_page(browser: RoboBrowser) -> bool:
    if browser.state.response.content is None:
        logger.warning("request content failed")
        return True

    pagelink = browser.find(class_='pagelink')
    if pagelink is None:
        logger.warning('no pages url: {}', browser.url)
        fid = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        logger.warning('response detail in: {}', fid+'.html')
        fail_file_path = os.path.join(base_path, 'pages', fid+'.html')
        with open(fail_file_path, 'wb') as f:
            f.write(browser.state.response.content)
        return True
    
    if pagelink.find(class_='next') is None:
        return True

    return False

def next_page(browser: RoboBrowser) -> Tag:
    pagelink = browser.find(class_='pagelink')
    return pagelink.find(class_='next')


def get_novels(browser: RoboBrowser):
    return [li for li in browser.find(class_="l").ul][1:-1]


def get_id(novel: Tag):
    return novel.find(class_='s2').a['href'].split('/')[3]

def get_title(novel: Tag):
    return novel.find(class_='s2').a.string

def get_author(novel: Tag):
    return novel.find(class_='s5').string

def get_date(novel: Tag):
    return novel.find(class_='s3').contents[1]

def get_link(novel: Tag):
    return novel.find(class_='s2').a['href']

def get_novel_info(novel: Tag):
    return {
        'id': get_id(novel), 'title': get_title(novel),
        'author': get_author(novel), 'date': get_date(novel),
        'link': get_link(novel), 'chapter': '0/0',
    }

def get_novel_content(info):
    browser = RoboBrowser(parser='html5lib', history=True,
                          timeout=30, tries=5, multiplier=0.3)

    try:
        browser.open(info['link'])
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        logger.error('', url=info['link'], err=e)
        return ''
    except:
        logger.exception('request failed: {url}', url=info['link'])
        return ''
    
    chapter_contents = []
    chapters_link = get_chapters_link(browser)
    chapter_total = len(chapters_link)
    chapter_count = 1
    for chapter_link in chapters_link:
        time.sleep(random.randint(2, 5))
        try:
            browser.follow_link(chapter_link)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            logger.error('', url=browser.url, err=e)
            break
        except:
            logger.exception('request failed: {url}', url=browser.url)
            break
        chapter_contents.append(get_chapter_content(browser))
        chapter_count += 1
    
    if len(chapter_contents) == 0:
        logger.info('void novel detail is \n{}', browser.find())
    
    info['chapter'] = str(chapter_count) + '/' + str(chapter_total)

    return '\n'.join(chapter_contents)


def get_chapters_link(browser: RoboBrowser):
    chapters_link = []
    for d in set(browser.find(id="list").dl.contents):
        if d.name == 'dd':
            chapters_link.append(d.a)
    return chapters_link


def get_chapter_content(browser: RoboBrowser):
    chapter_name = browser.find(class_="bookname").h1.string
    chapter_content = '\n'.join(filter(lambda x: x != '', [line.strip() for line in browser.find(id="content").strings]))
    return chapter_name + '\n' + chapter_content
