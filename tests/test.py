from robobrowser import RoboBrowser

url = 'https://hs.etet.men/read.php?tid=3337712&page=2'

def open():
    browser = RoboBrowser(history=True, parser='html5lib', timeout=30)
    browser.open(url)

    print(browser.parsed())

if __name__ == "__main__":
    open()