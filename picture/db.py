import sqlite3
from pathlib import Path

base_path = Path(__file__).parent

sql_read = """
    SELECT *
    FROM picture_miss
"""

sql_insert = """
    INSERT
    INTO picture_miss(title, url, filename)
    VALUES (?, ?, ?)
"""

sql_delete = """
    DELETE
    FROM picture_miss
    WHERE url = ?
"""


class Database(object):
    def __init__(self, filename):
        self.filename = filename

    def init(self):
        with open(str(base_path / "schema.sql"), 'r') as f:
            with self.db() as db:
                db.executescript(f.read())

    def db(self):
        return sqlite3.connect(str(base_path / self.filename),
                               detect_types=sqlite3.PARSE_DECLTYPES)

    def read(self):
        with self.db() as db:
            rows = db.execute(sql_read)

        result = []
        for row in rows:
            r = {}
            r["id"], r["title"], r["url"], r["filename"], _ = row
            result.append(r)
        return result

    def insert(self, title, url, filename):
        with self.db() as db:
            db.execute(sql_insert, (title, url, filename))

    def delete(self, url):
        with self.db() as db:
            db.execute(sql_delete, (url,))
