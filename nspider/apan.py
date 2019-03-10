"""save novel content into anyview website
"""
import os

from robobrowser import RoboBrowser, forms

APAN_URL = 'http://apanr.net/'
USERNAME = 'tengshan2008'
PASSWORD = '8443658y'


def login(username, password, url):
    browser = RoboBrowser(history=True)
    browser.open(url)
    # login
    login_form = browser.get_form(id='log-in')
    login_form['account'].value = username
    login_form['password'].value = password
    browser.submit_form(login_form)
    # access account
    account = browser.find(href='/account')
    browser.follow_link(account)
    return browser


def upload(novel_info, content):
    browser = login(USERNAME, PASSWORD, APAN_URL)
    delete(browser, novel_info['title'])
    upload_form = browser.get_forms()[0]
    # add upload action field
    upload_action_str = '<input type="hidden" \
        name="action" value="upload_file_post" />'
    upload_action = forms.fields.Input(upload_action_str)
    upload_form.add_field(upload_action)
    # add upload file field
    path = os.path.join('novels', novel_info['title'] + '.txt')
    # submit upload form
    with open(path, 'w', encoding='utf-8') as f:
        f.write(file_content(novel_info, content))
    with open(path, 'r', encoding='utf-8') as f:
        upload_form['file_to_upload'].value = f
        browser.submit_form(upload_form)
    # delete temp file
    if os.path.exists(path):
        os.remove(path)


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
