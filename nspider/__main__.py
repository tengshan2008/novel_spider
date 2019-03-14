from loguru import logger

from nspider import config, crawel, db

if __name__ == "__main__":
    # init database
    db.init()
    logger.success('database init success')

    # run crawel spider
    start_url = config.get('t66y', 'BaseUrl') + '/thread0806.php?fid=20'
    crawel.run(start_url)
