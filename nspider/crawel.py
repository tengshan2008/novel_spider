"""crawel t66y website novels
"""

import datetime
import random
import re
import time

from robobrowser import RoboBrowser

from nspider import apan, config, db, logger

NEXT_PAGE = '下一頁'
TODAY = '今天'
YESTERDAY = '昨天'
PATTERN = '草榴官方客戶端|來訪者必看的內容|发帖前必读|关于论坛的搜索功能|文学区违规举报专贴|文區版規'


def run(url):
    browser = RoboBrowser(parser='html.parser', history=True,
                          timeout=30, tries=5)

    try:
        browser.open(url)
    except:
        logger.error('request failed:' + url)

    dbase = db.get()

    while not is_end_page(browser):
        for novel in get_novels(browser):
            time.sleep(5)
            novel_info = get_info(novel)
            # logger.debug(novel_info)
            logger.info(novel_info['title'])
            content = get_content(novel_info)
            novel_info['size'] = len(content)
            if db.insert(novel_info, dbase):
                apan.upload(novel_info, content)

        try:
            browser.follow_link(next_page(browser))
        except:
            logger.error('request failed: ' + browser.url)
            return

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
        if page.string == NEXT_PAGE:
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
        return True

    for label_a in browser.find_all('a'):
        if label_a.string == NEXT_PAGE:
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
    return config.get('t66y', 'BaseUrl') + '/' + novel.find('td', class_='tal').h3.a['href'].strip()


def get_content(info):
    browser = RoboBrowser(parser='html.parser', history=True,
                          timeout=30, tries=5)
    try:
        browser.open(info['link'])
    except:
        logger.error('request failed: ' + info['link'])
        return ''

    contents = []
    while not is_end_page(browser):
        time.sleep(5)
        contents.append(get_cell_content(browser, info['author']))
        try:
            browser.follow_link(next_page(browser))
        except:
            logger.error('request failed: ' + browser.url)

    return '\n'.join(contents)


def get_cell_content(browser, author):
    content = []
    for cell in browser.find_all(class_='t t2'):
        if cell.find(class_='r_two').b.string == author:
            for cell_content in cell.find(class_=['tpc_content do_not_catch',
                                          'tpc_content']).strings:
                content.append(cell_content.strip())
    return '\n'.join(content)
