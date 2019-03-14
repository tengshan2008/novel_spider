"""save novel info into database
"""

import sqlite3
from os import path

from nspider import config

base_path = path.split(path.realpath(__file__))[0]
sql = """
    INSERT
    INTO novel(nid, title, author, ndate, ntype, link)
    VALUES (?, ?, ?, ?, ?, ?)
"""

def get():
    db_path = path.join(base_path, config.get('sqlite', 'File'))
    db = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    return db


def close(db):
    if db is not None:
        db.close()


def init():
    db = get()
    script_path = path.join(base_path, 'schema.sql')
    with open(script_path, 'r') as f:
        try:
            with db:
                db.executescript(f.read())
        except sqlite3.OperationalError as e:
            print("init db error:", e)
        finally:
            close(db)


def insert(novel_info, db):
    novel_info = {k: v.replace("'", "''") for k, v in novel_info.items()}

    try:
        with db:
            db.execute(sql, (int(novel_info['id']), novel_info['title'],
                             novel_info['author'], novel_info['date'],
                             novel_info['type'], novel_info['link']))
    except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
        print('Could not complete operation:', e)
        return False

    return True


if __name__ == "__main__":
    init()
