from caoliu import crawel, db, logger, apan
from util import config

if __name__ == "__main__":
    # init database
    db.init()

    # apan login
    username = config.get('apan', 'User')
    password = config.get('apan', 'Pass')
    apan_url = config.get('apan', 'Url')
    apan_browser = apan.login(username, password, apan_url)

    # run crawel spider
    base_url = config.get('t66y', 'BaseUrl')
    start_url = base_url + '/thread0806.php?fid=20'
    for i in range(10):
        crawel.run(start_url, apan_browser)
