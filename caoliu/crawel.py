"""crawel t66y website novels
"""

import datetime
import os
import random
import re
import string
import time

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from robobrowser import RoboBrowser

from caoliu import apan, db, errors, logger
from util import config, proxy_pool

NEXT_PAGE = '下一'
TODAY = '今天'
YESTERDAY = '昨天'
PATTERN = '草榴官方客戶端|來訪者必看的內容|发帖前必读|关于论坛的搜索功能|文学区违规举报专贴|文區版規'

base_path = path.split(path.realpath(__file__))[0]


def run(url: str, idx: int):
    browser = RoboBrowser(parser='html5lib', history=True,
                          timeout=30, tries=5, multiplier=0.3)

    try:
        browser.open(url)
    except (requests.exceptions.Timeout, requests.ConnectionError) as e:
        logger.error(errors.RequestsFail, url=url, err=e)
        return
    except:
        logger.exception('request failed: {url}', url=url)
        return

    if need_redirects(browser):
        redirect_link = redirect(browser)
        try:
            browser.follow_link(redirect_link)
        except (requests.exceptions.Timeout, requests.ConnectionError) as e:
            logger.error(errors.RequestsFail, url=browser.url, err=e)
            return
        except:
            logger.exception('request failed: {url}', url=browser.url)
            return

    db_file = config.get('sqlite', 'caoliu')
    dbase = db.get(db_file)

    count = idx + 1
    while True:
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
        if is_end_page(browser):
            break
        try:
            browser.follow_link(next_page(browser))
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
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

    if browser.state.response.content is None:
        logger.warning('request content failed')
        return True

    if browser.find(class_='pages') is None:
        logger.warning('no pages url: {}', browser.url)
        fid = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        logger.warning('response detail in: \n{}', fid+'.html')
        fail_file_path = os.path.join(base_path, 'pages', fid+'.html')
        with open(fail_file_path, 'wb') as f:
            f.write(browser.state.response.content)
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
        'type': get_type(novel), 'link': get_link(novel),
        'page': '0/0',
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


def get_content(info: dict):
    browser = RoboBrowser(parser='html5lib', history=True,
                          timeout=30, tries=5, multiplier=0.3)
    proxies = {'https': proxy_pool.get_random()}

    try:
        browser.open(info['link'])
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
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
        except (requests.exceptions.Timeout, requests.ConnectionError) as e:
            logger.error(errors.RequestsFail, url=browser.url, err=e)
            return ''
        except:
            logger.exception('request failed: {url}', url=browser.url)
            return ''

    page_total = '0'
    page_count = 1
    contents = []
    while True:
        time.sleep(random.randint(2, 5))
        contents.append(get_cell_content(browser, info['author']))
        if is_end_page(browser):
            break
        page_total = find_total_page(browser)
        try:
            browser.follow_link(next_page(browser), proxies=proxies)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            logger.error(errors.RequestsFail, url=browser.url, err=e)
            logger.error('proxy is: {}', proxies)
            break
        except requests.exceptions.ProxyError as e:
            logger.error(errors.RequestsFail, url=browser.url, err=e)
            logger.error('proxy is: {}', proxies)
            break
        except:
            logger.exception('request failed: {url}', url=browser.url)
            logger.error('proxy is: {}', proxies)
            break
        page_count += 1

    if len(contents) == 0:
        logger.info('void novel detail is \n{}', browser.find())

    info['page'] = str(page_count) + '/' + page_total

    return '\n'.join(contents)


def get_cell_content(browser: RoboBrowser, author: str) -> str:
    content = []
    for cell in browser.find_all(class_='t t2'):
        if cell.find(class_='r_two').b.string == author:
            for cell_content in cell.find(class_=['tpc_content do_not_catch',
                                          'tpc_content']).strings:
                content.append(cell_content.strip())
    return '\n'.join(content)


def find_total_page(browser: RoboBrowser):
    pages = browser.find(class_='pages')
    return pages.find_all('a')[-1]['href'].split('=')[-1]


def need_redirects(browser: RoboBrowser) -> bool:
    state = browser.state.response.text
    bs = BeautifulSoup(state.replace('<!---->', ''), 'html5lib')
    return len(bs.find_all('a')) == 2


def redirect(browser: RoboBrowser) -> Tag:
    state = browser.state.response.text
    bs = BeautifulSoup(state.replace('<!---->', ''), 'html5lib')
    redirect_link = bs.find_all('a')[1]
    return redirect_link
