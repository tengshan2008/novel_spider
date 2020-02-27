import tempfile

from mechanicalsoup import StatefulBrowser as Browser

username = 'tengshan201'
password = 'QNMG5FVJHEYEWyk6'


class ApanManager(object):
    def __init__(self, host=None):
        if host is not None:
            self.login_host = host
        self.login_host = 'http://apanr.net/login'
        self.browser = Browser()

    def login(self, username, password):
        """login
        """
        self.browser.open(self.login_host)

        self.browser.select_form('#log-in')
        self.browser["account"] = username
        self.browser["password"] = password
        self.browser.submit_selected()

        soup = self.browser.get_current_page()
        if soup.head.title.string == "登录成功":
            buttons = soup.body("div", class_="buttons")
            redirect_my_account = buttons[0]('a')[1]
            self.browser.follow_link(redirect_my_account)

    def upload(self, path):
        self.browser.select_form('#upload-file-form')
        self.browser.new_control("", "action", "upload_file_xhr")
        self.browser.new_control("file", "file_to_upload", path)
        self.browser.submit_selected()

    def remove(self, file_id):
        soup = self.browser.get_current_page()
        remove_form = soup.find_all('form')[1]
        self.browser.select_form(remove_form)
        self.browser.new_control("", "action", "del_file")
        self.browser.new_control("", "file_id", file_id)
        self.browser.submit_selected()

    def download(self, file_id, file_name, file_link):
        self.browser.download_link(file_link, file_name)

    def get_list(self):
        soup = self.browser.get_current_page()
        upload_list = soup.find_all("div", id="upload-list")[0]
        forms = upload_list.find_all("form")
        if len(forms) > 1:
            item_list = forms[1].table.tbody.find_all("tr")
        result = []
        for item in item_list:
            item_title, item_down, item_del = item.find_all("td")
            result.append(Item(item_title.string.strip(),
                               item_del.button["value"],
                               item_down.a["href"],
                               self.browser))
        return result


class Item(ApanManager):
    def __init__(self, title, id, link, browser):
        self.title = title
        self.id = id
        self.link = link
        self.browser = browser

    def remove(self):
        super().remove(self.id)

    def download(self):
        super().download(self.id, self.title, self.link)


if __name__ == "__main__":
    am = ApanManager()
    # login
    am.login(username, password)

    # upload file
    # am.upload("pipline/测试文件2.txt")

    # get apan list
    for item in am.get_list():
        # if item.id == '26192840':
        #     item.remove()
        print(item.id, item.title)

    # download file
    # am.download(item.id, item.title, item.link)

    # remove file
    # am.remove(26173139)
