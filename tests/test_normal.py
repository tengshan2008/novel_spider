from mechanicalsoup import StatefulBrowser as Browser


def open_html(url):
    soup = None
    with Browser() as browser:
        browser.open(url)
        soup = browser.get_current_page()
    return soup


def video_source(url):
    soup = open_html(url)
    print(soup)


def video_frame(url):
    soup = open_html(url)
    main = soup.body.find_all("div", id="main", recursive=False)[0]
    tpc_cont = main.find_all("div", class_="tpc_cont", recursive=False)[0]
    print(tpc_cont)


if __name__ == "__main__":
    # url = "https://cl.fr67.ga/htm_mob/2001/22/3776206.html"
    # video_frame(url)
    url = "https://jjdong5.com/embed/2431"
    video_source(url)
