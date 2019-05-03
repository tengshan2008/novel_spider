"""save novel info into database
"""

import sqlite3
from os import path

from caoliu import logger
from util import config

base_path = path.split(path.realpath(__file__))[0]

sql_read = """
    SELECT size
    FROM novel
    WHERE nid = ?
"""

sql_insert = """
    INSERT
    INTO novel(nid, title, author, ndate, ntype, link, size)
    VALUES (?, ?, ?, ?, ?, ?, ?)
"""

sql_update = """
    UPDATE novel
    SET size = ?
    WHERE nid = ?
"""

sql_delete = """
    DELETE
    FROM  novel
    WHERE nid = ?
"""


def get(filename):
    db_path = path.join(base_path, filename)
    db = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    return db


def close(db):
    if db is not None:
        db.close()
        logger.info("database close")


def init():
    db_file = config.get('sqlite', 'caoliu')
    db = get(db_file)
    script_path = path.join(base_path, 'schema.sql')
    with open(script_path, 'r') as f:
        try:
            with db:
                db.executescript(f.read())
            logger.info("database init success")
        except sqlite3.OperationalError as e:
            logger.error("init db error: {}", e)
        except:
            logger.exception('detail')
        finally:
            close(db)


def insert(novel_info: dict, db):
    novel_info = {k: v.replace("'", "''") for k, v in novel_info.items()}

    try:
        with db:
            size = db.execute(sql_read, (int(novel_info['id']),)).fetchone()
            if size is None:
                logger.info("insert {}, page {}",
                            novel_info['title'],
                            novel_info['page'])
                db.execute(sql_insert, (int(novel_info['id']),
                                        novel_info['title'],
                                        novel_info['author'],
                                        novel_info['date'],
                                        novel_info['type'],
                                        novel_info['link'],
                                        int(novel_info['size'])),)
            elif int(novel_info['size']) > size[0]:
                logger.info("update {}, page {}",
                            novel_info['title'],
                            novel_info['page'])
                db.execute(sql_update, (int(novel_info['size']),
                                        int(novel_info['id'])))
            else:
                logger.info("ignore {}, page {}",
                            novel_info['title'],
                            novel_info['page'])
                return False

    except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
        logger.error('Could not complete operation, error: {}', e)
        return False
    except ValueError as e:
        logger.error('novel info {} has wrong value', novel_info)
        return False
    except:
        logger.exception('detail')
        return False

    return True


def delete(novel_info, db):
    try:
        with db:
            db.execute(sql_delete, (int(novel_info['id']),))
    except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
        logger.error('Could not complete operation, error: {}', e)
    except:
        logger.exception('detail')


if __name__ == "__main__":
    init()
