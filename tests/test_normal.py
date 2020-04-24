from mechanicalsoup import StatefulBrowser as Browser
from urllib.parse import urlparse


def filter_title(title):
    # Invaild symbol \ / : * ? < > |
    title = title.replace("\\", '')
    title = title.replace('/', '')
    title = title.replace(':', '：')
    title = title.replace('*', '')
    title = title.replace('?', '？')
    title = title.replace('<', '《')
    title = title.replace('>', '》')
    title = title.replace('|', '')
    title = title.replace('(', '（')
    title = title.replace(')', '）')
    title = title.replace(' ', '')
    return title


def open_html(url):
    soup = None
    with Browser() as browser:
        try:
            browser.open(url)
        except Exception as e:
            print(e)
            return None
        soup = browser.get_current_page()
    return soup


def video_source(url):
    soup = open_html(url)
    if soup is None:
        return None
    if "-video" in soup.head.title.string:
        golinks = soup.body.find_all("div", class_="golink")
        if len(golinks) != 0:
            host = golinks[0].a.string.replace('立即访问：', '').strip()
            return host
        else:
            return None
    else:
        return None


def video_frame(url):
    soup = open_html(url)
    main = soup.body.find_all("div", id="main", recursive=False)[0]
    tpc_cont = main.find_all("div", class_="tpc_cont", recursive=False)[0]
    form = main.find_all("form", recursive=False)[0]
    input_class = form.div.table.find_all("input", class_="input")[0]
    title = filter_title(input_class['value'])
    _, in_a = tpc_cont.find_all("a", recursive=False)
    source_link = in_a["onclick"].split('=')[1][1:-12]
    return title, source_link


if __name__ == "__main__":
    url = "http://cl.dn37.xyz/htm_mob/2001/22/3776206.html"
    title, source_link = video_frame(url)
    # print(f"you-get -d {source_link} -O \"{title}\"")
    host = video_source(source_link)
    if host is not None:
        parsed = urlparse(source_link)
        source_link = parsed._replace(netloc=host).geturl()
    print(f"you-get -d {source_link} -O \"{title}\"")
