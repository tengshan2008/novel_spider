from robobrowser import RoboBrowser

url = 'https://hs.etet.men/read.php?tid=3337712&page=2'

user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'

def open():
    browser = RoboBrowser(history=True, parser='html5lib', 
                          timeout=30, user_agent=user_agent)
    browser.open(url)

    print(browser.parsed())

if __name__ == "__main__":
    open()