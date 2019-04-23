import time

from caoliu import apan, crawel, db, logger
from util import config

if __name__ == "__main__":
    # init database
    db.init()

    # get caoliu config
    base_url = config.get('t66y', 'BaseUrl')
    start_url = base_url + '/thread0806.php?fid=20'

    # run crawel spider 10 times
    for i in range(10):
        # crawel run
        time.sleep(20)
        crawel.run(start_url)
