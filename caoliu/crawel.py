"""crawel t66y website novels
"""

import datetime
import random
import re
import time

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from robobrowser import RoboBrowser

from caoliu import apan, db, errors, logger
from util import config

NEXT_PAGE = '下一'
TODAY = '今天'
YESTERDAY = '昨天'
PATTERN = '草榴官方客戶端|來訪者必看的內容|发帖前必读|关于论坛的搜索功能|文学区违规举报专贴|文區版規'

user_agent = '''Mozilla/5.0 (Windows NT 10.0; Win64; x64)
                AppleWebKit/537.36 (KHTML, like Gecko)
                Chrome/73.0.3683.75 Safari/537.36'''

ip_pool = [
        '221.11.105.68:56120',
        '222.189.191.9:9999',
        '116.209.57.6:9999',
        '219.159.38.201:56210',
        '114.249.119.52:9000',
        '122.193.244.126:9999',
        '118.187.58.35:53281',
        '116.209.58.85:9999',
        '125.123.140.201:9999',
        '163.125.223.214:8118'
    ]


def run(url: str, idx: int):
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

    if need_redirects(browser):
        redirect_link = redirect(browser)
        try:
            browser.follow_link(redirect_link)
        except requests.ConnectionError as e:
            logger.error(errors.RequestsFail, url=browser.url, err=e)
            return
        except:
            logger.exception('request failed: {url}', url=browser.url)
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


def get_novels(browser: RoboBrowser) -> list:
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


def next_page(browser: RoboBrowser) -> Tag:
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


def is_end_page(browser: RoboBrowser) -> bool:
    """ lookup the end page

    Arguments:
        browser {Robobrowser} -- browser object

    Returns:
        Boolean -- judge the end page
    """

    if browser.find(class_='pages') is None:
        logger.debug('no pages detail: {}', browser.url)
        logger.debug('request headers: {}', browser.session.headers)
        logger.debug('resp :{}', browser.state.response.content.decode('gbk'))
        logger.debug('response code: {}', browser.state.response.status_code)
        logger.debug('beautiful soup parse: {}', browser.parsed()[0])
        return True

    for label_a in browser.find_all('a'):
        if label_a.string is not None and NEXT_PAGE in label_a.string:
            if label_a.get('href') == 'javascript:#':
                return True

    return False


def get_info(novel: Tag) -> dict:
    return {
        'id': get_id(novel), 'title': get_title(novel),
        'author': get_author(novel), 'date': get_date(novel),
        'type': get_type(novel), 'link': get_link(novel)
    }


def get_id(novel: Tag) -> str:
    href = novel.find('td', class_='tal').a['href']
    return href.split('/')[-1].split('.')[0]


def get_title(novel: Tag) -> str:
    return novel.find('td', class_='tal').a.string.strip()


def get_author(novel: Tag) -> str:
    return novel.find('a', class_='bl').string.strip()


def get_type(novel: Tag) -> str:
    return novel.find(class_='tal').contents[0].strip()


def get_date(novel: Tag) -> str:
    date = novel.find('div', class_='f12').string
    if TODAY in date:
        return str(datetime.date.today())
    if YESTERDAY in date:
        return str(datetime.date.today() - datetime.timedelta(days=1))
    return date


def get_link(novel: Tag) -> str:
    base_url = config.get('t66y', 'BaseUrl')
    return base_url + '/' + novel.find('td', class_='tal').h3.a['href'].strip()


def get_content(info: dict) -> str:
    session = requests.Session()
    session.proxies = {'https': random.choice(ip_pool)}
    browser = RoboBrowser(parser='html5lib', history=True, session=session,
                          timeout=30, tries=5, multiplier=0.3)
    # browser.session.headers['User-Agent'] = user_agent

    try:
        browser.open(info['link'])
    except requests.ConnectionError as e:
        logger.error(errors.RequestsFail, url=info['link'], err=e)
        return ''
    except:
        logger.exception('request failed: {url}', url=info['link'])
        return ''

    if need_redirects(browser):
        redirect_link = redirect(browser)
        try:
            browser.follow_link(redirect_link)
            logger.debug('new link is {}', browser.url)
        except requests.ConnectionError as e:
            logger.error(errors.RequestsFail, url=browser.url, err=e)
            return ''
        except:
            logger.exception('request failed: {url}', url=browser.url)
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


def get_cell_content(browser: RoboBrowser, author: str) -> str:
    content = []
    for cell in browser.find_all(class_='t t2'):
        if cell.find(class_='r_two').b.string == author:
            for cell_content in cell.find(class_=['tpc_content do_not_catch',
                                          'tpc_content']).strings:
                content.append(cell_content.strip())
    return '\n'.join(content)


def need_redirects(browser: RoboBrowser) -> bool:
    state = browser.state.response.text
    bs = BeautifulSoup(state.replace('<!---->', ''), 'html5lib')
    return len(bs.find_all('a')) == 2


def redirect(browser: RoboBrowser) -> Tag:
    state = browser.state.response.text
    bs = BeautifulSoup(state.replace('<!---->', ''), 'html5lib')
    redirect_link = bs.find_all('a')[1]
    return redirect_link
