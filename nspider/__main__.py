from nspider.crawel import run
from nspider import getConfig

if __name__ == "__main__":
    start_url = getConfig('t66y', 'BaseUrl') + '/thread0806.php?fid=20'
    run(start_url)