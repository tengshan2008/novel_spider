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
    c = db.cursor()
    with open('schema.sql', 'r') as f:
        try:
            with c:
                c.executescript(f.read())
        except sqlite3.OperationalError as e:
            print("init db error:", e)
        finally:
            c.close()
            close_db(db)


def insert(novel_info):
    db = get_db()
    c = db.cursor()
    with c:
        c.execute("SELECT * FROM novel WHERE nid = ?", (novel_info['id'],))
        c.fetchone()

        c.execute("INSERT INTO novel(nid, title, author, ndate, ntype, link) values (?, ?, ?, ?, ?)", (
            int(novel_info['id']), novel_info['title'], novel_info['author'], novel_info['date'], 
            novel_info['type'], novel_info['link']))

    c.close()
    close_db(db)


if __name__ == "__main__":
    init_db()
