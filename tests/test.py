from robobrowser import RoboBrowser
import requests

url = 'https://hs.etet.men/htm_data/20/1811/3352869.html'


def open():
    browser = RoboBrowser(history=True, parser='html5lib',
                          timeout=10)

    browser.open(url, proxies={'https': '182.92.105.136:3128'})
    # browser.open(url)

    print(browser.session.headers)

    print(browser.state.response.content.decode('gbk'))

    print(browser.parsed()[0])


if __name__ == "__main__":
    open()
