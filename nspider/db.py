"""save novel info into database
"""

import sqlite3

from configparser import ConfigParser

conf = ConfigParser()
conf.read("app.config")


def get_db():
    db = sqlite3.connect("novel.db", detect_types=sqlite3.PARSE_DECLTYPES)
    return db


def close_db(db):
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with open('schema.sql', 'r') as f:
        try:
            with db:
                db.executescript(f.read())
        except sqlite3.OperationalError as e:
            print("init db error:", e)
        finally:
            close_db(db)


def insert(novel_info, db):
    novel_info = {k: v.replace("'", "''") for k, v in novel_info.items()}

    try:
        with db:
            db.execute("INSERT INTO novel(nid, title, author, ndate, ntype, link) \
                values (?, ?, ?, ?, ?, ?)", (
                int(novel_info['id']), novel_info['title'],
                novel_info['author'], novel_info['date'],
                novel_info['type'], novel_info['link']))
    except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
        print('Could not complete operation:', e)
        return False

    return True


if __name__ == "__main__":
    init_db()
