"""crawel t66y website novels
"""

import datetime
import random
import re
import time

import requests
from robobrowser import RoboBrowser

from caoliu import apan, db, logger, errors
from util import config

NEXT_PAGE = '下一'
TODAY = '今天'
YESTERDAY = '昨天'
PATTERN = '草榴官方客戶端|來訪者必看的內容|发帖前必读|关于论坛的搜索功能|文学区违规举报专贴|文區版規'


def run(url, idx):
    browser = RoboBrowser(parser='html5lib', history=True,
                          timeout=30, tries=5, multiplier=0.3)

    try:
        browser.open(url)
    except requests.ConnectionError as e:
        logger.error(errors.RequestsFail, url=url, err=e)
        return
    except:
        logger.exception('request failed: {url}', url=url)
        return

    db_file = config.get('sqlite', 'caoliu')
    dbase = db.get(db_file)

    count = idx + 1
    while not is_end_page(browser):
        logger.info("current page is {}", count)
        for novel in get_novels(browser):
            time.sleep(random.randint(2, 5))
            novel_info = get_info(novel)
            content = get_content(novel_info)
            novel_info['size'] = str(len(content))
            if db.insert(novel_info, dbase):
                ok = apan.upload(novel_info, content)
                if not ok:
                    db.delete(novel_info, dbase)
        page_link = next_page(browser)
        if page_link is None:
            logger.error("get next page failed")
            logger.info('detail\n{}', browser.find())
            db.close(dbase)
            return
        try:
            browser.follow_link(page_link)
        except requests.ConnectionError as e:
            logger.error(errors.RequestsFail, url=browser.url, err=e)
            db.close(dbase)
            return
        except:
            logger.exception('request failed: {url}', url=browser.url)
            db.close(dbase)
            return
        count += 1

    db.close(dbase)


def get_novels(browser):
    """ get all novels link

    Arguments:
        browser {Robobrowser} -- browser object

    Returns:
        string -- one page all novels info
    """

    novels = []
    for tr in browser.select('tr.tr3.t_one.tac'):
        if re.search(PATTERN, tr.h3.a.string) is None:
            novels.append(tr)
    return novels


def next_page(browser):
    """get next page link

    Arguments:
        browser {Robobrowser} -- browser object

    Returns:
        string -- url link
    """

    pages = browser.find(class_='pages')
    for page in pages:
        if page.string is not None and NEXT_PAGE in page.string:
            return page
    return None


def is_end_page(browser):
    """ lookup the end page

    Arguments:
        browser {Robobrowser} -- browser object

    Returns:
        Boolean -- judge the end page
    """

    if browser.find(class_='pages') is None:
        logger.debug('no pages detail: {}', browser.url)
        for state in browser._states:
            logger.debug(state.response.content.decode('utf-8', 'replace'))
        return True

    for label_a in browser.find_all('a'):
        if label_a.string is not None and NEXT_PAGE in label_a.string:
            if label_a.get('href') == 'javascript:#':
                return True

    return False


def get_info(novel):
    return {
        'id': get_id(novel), 'title': get_title(novel),
        'author': get_author(novel), 'date': get_date(novel),
        'type': get_type(novel), 'link': get_link(novel)
    }


def get_id(novel):
    href = novel.find('td', class_='tal').a['href']
    return href.split('/')[-1].split('.')[0]


def get_title(novel):
    return novel.find('td', class_='tal').a.string.strip()


def get_author(novel):
    return novel.find('a', class_='bl').string.strip()


def get_type(novel):
    return novel.find(class_='tal').contents[0].strip()


def get_date(novel):
    date = novel.find('div', class_='f12').string
    if TODAY in date:
        return str(datetime.date.today())
    if YESTERDAY in date:
        return str(datetime.date.today() - datetime.timedelta(days=1))
    return date


def get_link(novel):
    base_url = config.get('t66y', 'BaseUrl')
    return base_url + '/' + novel.find('td', class_='tal').h3.a['href'].strip()


def get_content(info):
    browser = RoboBrowser(parser='html5lib', history=True,
                          timeout=30, tries=5, multiplier=0.3)
    try:
        browser.open(info['link'])
    except requests.ConnectionError as e:
        logger.error(errors.RequestsFail, url=info['link'], err=e)
        return ''
    except:
        logger.exception('request failed: {url}', url=info['link'])
        return ''

    contents = []
    while not is_end_page(browser):
        time.sleep(random.randint(2, 5))
        contents.append(get_cell_content(browser, info['author']))
        page_link = next_page(browser)
        if page_link is None:
            logger.error("get next page failed")
            logger.info("detail\n{}", browser.find())
            break
        try:
            browser.follow_link(page_link)
        except requests.ConnectionError as e:
            logger.error(errors.RequestsFail, url=browser.url, err=e)
            break
        except:
            logger.exception('request failed: {url}', url=browser.url)
            break

    if len(contents) == 0:
        logger.info('void novel detail is \n{}', browser.find())

    return '\n'.join(contents)


def get_cell_content(browser, author):
    content = []
    for cell in browser.find_all(class_='t t2'):
        if cell.find(class_='r_two').b.string == author:
            for cell_content in cell.find(class_=['tpc_content do_not_catch',
                                          'tpc_content']).strings:
                content.append(cell_content.strip())
    return '\n'.join(content)
