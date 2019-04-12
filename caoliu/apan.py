"""save novel content into anyview website
"""
import time
from os import path, remove

from robobrowser import RoboBrowser, forms

from caoliu import logger
from util import config

base_path = path.split(path.realpath(__file__))[0]


def login(username, password, url):
    browser = RoboBrowser(parser='html.parser', history=True,
                          timeout=30, tries=5, multiplier=0.3)

    try:
        browser.open(url)
    except Exception as e:
        logger.error('request failed: {url}', url=url)
        logger.exception('detail')

    # login
    login_form = browser.get_form(id='log-in')
    login_form['account'].value = username
    login_form['password'].value = password
    browser.submit_form(login_form)
    # access account
    account = browser.find(href='/account')
    if account is None:
        logger.info("page detail is: \n{}", browser.find())
        return None
    try:
        browser.follow_link(account)
    except Exception as e:
        logger.error('request failed: {url}', url=browser.url)
        logger.exception('detail')

    return browser


def upload(novel_info, content):
    # get apan config
    username = config.get('apan', 'User')
    password = config.get('apan', 'Pass')
    apan_url = config.get('apan', 'Url')
    # login
    browser = login(username, password, apan_url)
    if browser is None:
        logger.error("login apan failed")
        time.sleep(10)
        return
    # delete
    delete(browser, novel_info['title'])
    upload_form = browser.get_forms()[0]
    # add upload action field
    upload_action_str = '<input type="hidden" \
        name="action" value="upload_file_post" />'
    upload_action = forms.fields.Input(upload_action_str)
    upload_form.add_field(upload_action)
    # add upload file field
    pth = path.join(base_path, 'novels', novel_info['title'] + '.txt')
    # submit upload form
    try:
        with open(pth, 'w', encoding='utf-8') as f:
            f.write(file_content(novel_info, content))
    except (OSError, IOError) as e:
        logger.error('write file error: {}', e)
        logger.exception('detail')
        return
    try:
        with open(pth, 'r', encoding='utf-8') as f:
            upload_form['file_to_upload'].value = f
            browser.submit_form(upload_form)
    except (OSError, IOError) as e:
        logger.error('read file error: {}', e)
        logger.exception('detail')
        return
    # delete temp file
    write_in_local = config.getboolean('app', 'WriteInLocal')
    if not write_in_local and path.exists(pth):
        remove(pth)


def delete(browser, title):
    form = browser.get_forms()[1]
    # find old file and delete it
    table = browser.find(class_='table table-bordered table-striped')
    for tr in table.tbody.find_all('tr'):
        if title == tr.find('td', class_="item-title").string[1:-4]:
            button = tr.find('button')
            nid = button['value']
            delete_button_str = str(button)
            delete_action = forms.fields.Input(delete_button_str)
            form.add_field(delete_action)
            form['file_id'].value = nid
            browser.submit_form(form)
            break


def file_content(novel_info, content):
    return '\n'.join([
        '标题：' + novel_info['title'],
        '作者：' + novel_info['author'],
        '类型：' + novel_info['type'],
        '日期：' + novel_info['date'],
        content
    ])


if __name__ == "__main__":
    ni = {
        'id': 123,
        'title': '测试文件',
        'author': '大西瓜',
        'date': '2019-3-6',
        'type': '其他',
        'link': 'http://www.example.com'
    }
    content = '这是一个新的abc测试文件。\n'
    upload(ni, content)
