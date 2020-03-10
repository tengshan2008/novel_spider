"""save novel info into database
"""

import sqlite3
import os

# from util import config

base_path = os.path.split(os.path.realpath(__file__))[0]

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


class Database(object):
    def __init__(self, logger, filename):
        self.logger = logger
        self.db = self.get(filename)

    def get(self, filename):
        db_path = os.path.join(base_path, filename)
        db = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        return db

    def close(self):
        if self.db is not None:
            self.db.close()

    def init(self):
        script_path = os.path.join(base_path, 'schema.sql')
        with open(script_path, 'r') as f:
            try:
                with self.db:
                    self.db.executescript(f.read())
                self.logger.info("database init success")
            except sqlite3.OperationalError as e:
                self.logger.error("init db error: {}", e)
            except Exception:
                self.logger.exception('detail')
            finally:
                self.close()

    def insert(self, novel_info: dict):
        novel_info = {k: v.replace("'", "''") for k, v in novel_info.items()}

        try:
            with self.db:
                size = self.db.execute(sql_read,
                                       (int(novel_info['id']),)).fetchone()
                if size is None:
                    self.logger.info("insert {}, page {}",
                                     novel_info['title'],
                                     novel_info['page'])
                    self.db.execute(sql_insert, (int(novel_info['id']),
                                                 novel_info['title'],
                                                 novel_info['author'],
                                                 novel_info['date'],
                                                 novel_info['type'],
                                                 novel_info['link'],
                                                 int(novel_info['size'])),)
                elif int(novel_info['size']) > size[0]:
                    self.logger.info("update {}, page {}",
                                     novel_info['title'],
                                     novel_info['page'])
                    self.db.execute(sql_update, (int(novel_info['size']),
                                                 int(novel_info['id'])))
                else:
                    self.logger.info("ignore {}, page {}",
                                     novel_info['title'],
                                     novel_info['page'])
                    return False

        except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
            self.logger.error('Could not complete operation, error: {}', e)
            return False
        except ValueError as e:
            self.logger.error('novel info {} has wrong value', novel_info)
            return False
        except Exception:
            self.logger.exception('detail')
            return False

        return True

    def delete(self, novel_id):
        try:
            with self.db:
                self.db.execute(sql_delete, (int(novel_id),))
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
            self.logger.error('Could not complete operation, error: {}', e)
        except Exception:
            self.logger.exception('detail')


if __name__ == "__main__":
    from loguru import logger
    dbase = Database(logger, 'caoliu.db')
    dbase.get('test.db')
