from mechanicalsoup import StatefulBrowser as Browser


def git_test():
    url = 'http://cl.330f.tk/htm_mob/2002/7/3822632.html'
    browser = Browser()
    browser.open(url)
    soup = browser.get_current_page()
    for i, img in enumerate(soup.body.find_all('img')):
        browser.download_link(link=img["data-src"], file=f"{i}.gif", link_text='.git')



if __name__ == "__main__":
    git_test()
