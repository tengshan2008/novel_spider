from caoliu import crawel, db, logger, apan
from util import config

if __name__ == "__main__":
    # init database
    db.init()

    # get apan config
    username = config.get('apan', 'User')
    password = config.get('apan', 'Pass')
    apan_url = config.get('apan', 'Url')

    # get caoliu config
    base_url = config.get('t66y', 'BaseUrl')
    start_url = base_url + '/thread0806.php?fid=20'

    # run crawel spider 10 times
    for i in range(10):
        # apan login
        apan_browser = apan.login(username, password, apan_url)
        # crawel run
        crawel.run(start_url, apan_browser)
