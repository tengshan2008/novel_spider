from robobrowser import RoboBrowser
import requests

url = 'https://hs.etet.men/read.php?tid=3337712&page=2'

def open():
    session = requests.Session()
    session.headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': '__cfduid=daf1c243a21cc49f4807f162bc3a5ad6d1556430257; UM_distinctid=16a6278ff9b658-00d91e85434a76-7a1b34-144000-16a6278ff9c815; 227c9_lastvisit=0%091556591446%09%2Fread.php%3Ftid%3D3337712%26page%3D2; CNZZDATA950900=cnzz_eid%3D1797340401-1556428250-%26ntime%3D1556590258',
        'pragma': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }

    browser = RoboBrowser(history=True, parser='html5lib', 
                          timeout=30, session=session)

    browser.open(url)
    
    print(browser.state.response.headers)

    print(browser.parsed()[0])

if __name__ == "__main__":
    open()