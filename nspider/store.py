"""save novel content into anyview website
"""
import os

from robobrowser import RoboBrowser
from robobrowser import forms

apan_url = 'http://apanr.net/'


def store(novel_info, content):
    # delete(novel_info['title'])
    upload(novel_info, content)


def login():
    browser = RoboBrowser(history=True)
    browser.open(apan_url)
    # login
    login_form = browser.get_form(id='log-in')
    login_form['account'].value = 'tengshan2008'
    login_form['password'].value = '8443658y'
    browser.submit_form(login_form)
    # access account
    account = browser.find(href='/account')
    browser.follow_link(account)
    return browser

def upload(novel_info, content):
    browser = login()
    form = browser.get_forms()[0]
    # add upload action field
    upload_action_str = '<input type="hidden" name="action" value="upload_file_post" />'
    upload_action = forms.fields.Input(upload_action_str)
    form.add_field(upload_action)
    # add upload file field
    path = os.path.join('novels', novel_info['title'] + '.txt')
    file_input = '\n'.join([
            '标题：' + novel_info['title'],
            '作者：' + novel_info['author'],
            '类型：' + novel_info['type'],
            '日期：' + novel_info['date']
        ])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(file_input)
    with open(path, 'r', encoding='utf-8') as f:
        form['file_to_upload'].value = f
        print(f.read())
        browser.submit_form(form)
    # if os.path.exists(path):
    #     os.remove(path)

    

def delete(title):
    browser = login()
    form = browser.get_forms()[1]

    table = browser.find(class_='table table-bordered table-striped')
    for tr in table.tbody.find_all('tr'):
        if title == tr.find('td', class_="item-title").string[1:-4]:
            # print(title)
            button = tr.find('button')
            nid = button['value']
            delete_button_str = str(button)
            delete_action = forms.fields.Input(delete_button_str)
            form.add_field(delete_action)
            form['file_id'].value = nid
            browser.submit_form(form)
            break
    
if __name__ == "__main__":
    ni = {
        'id': 123,
        'title': '测试文件1',
        'author': '大西瓜',
        'date': '2019-3-4',
        'type': '其他',
        'link': 'http://www.example.com'
    }
    content = '这是一个测试文件。\n'
    store(ni, content)