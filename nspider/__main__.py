from nspider import config, db
from nspider.crawel import run

if __name__ == "__main__":
    # init database
    db.init()

    # run crawel spider
    start_url = config.get('t66y', 'BaseUrl') + '/thread0806.php?fid=20'
    run(start_url)
