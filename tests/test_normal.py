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
    _, in_a = tpc_cont.find_all("a", recursive=False)
    source_link = in_a["onclick"].split('=')[1][1:-12]
    return source_link


if __name__ == "__main__":
    url = "http://cl.hn32.xyz/htm_mob/2004/22/3890174.html"
    source_link = video_frame(url)
    print(source_link)
    # video_source(source_link)
