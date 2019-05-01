import time
# import random

from caoliu import apan, crawel, db, logger
from util import config

if __name__ == "__main__":
    # init database
    db.init()

    # get caoliu config
    base_url = config.get('t66y', 'BaseUrl')
    start_url = base_url + '/thread0806.php?fid=20'
    urls = [start_url + '&search=&page=' + str(i) for i in range(1, 25)]

    # run crawel spider 10 times
    for i in range(10):
        # crawel run
        time.sleep(20)
        url = random.choice(urls)
        # crawel.run(start_url, 0)
        crawel.run(url, urls.index(url))
