from robobrowser import RoboBrowser
import requests

url = 'https://hs.etet.men/read.php?tid=3337712&page=2'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'

def open():
    # session = requests.Session()
    # session.headers = {
    #     'Date': 'Tue, 30 Apr 2019 02:16:04 GMT', 
    #     'Content-Type': 'text/html', 
    #     'Transfer-Encoding': 'chunked', 
    #     'Connection': 'keep-alive', 
    #     'Set-Cookie': '__cfduid=d811bb4f9b359dd06254550b9c855c4af1556590564; expires=Wed, 29-Apr-20 02:16:04 GMT; path=/; domain=.etet.men; HttpOnly; Secure, 227c9_lastvisit=0%091556590564%09%2Fread.php%3Ftid%3D3337712%26page%3D2; expires=Wed, 29-Apr-2020 02:16:04 GMT; Max-Age=31536000; path=/',
    #     'X-Powered-By': 'PHP/5.6.33',
    #     'Vary': 'Accept-Encoding',
    #     'Expect-CT': 'max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"', 
    #     'Server': 'cloudflare', 
    #     'CF-RAY': '4cf602f1cb5e7892-LAX', 
    #     'Content-Encoding': 'gzip'
    # }

    browser = RoboBrowser(history=True, parser='html5lib', 
                          timeout=30, user_agent=user_agent)
    browser.open(url)
    
    # print(browser.state.response.headers)

    print(browser.parsed()[0])

if __name__ == "__main__":
    open()