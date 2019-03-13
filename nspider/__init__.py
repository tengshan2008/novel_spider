import sys
import configparser
from os import path
from nspider.db import get_db, close_db

if sys.version_info < (3, 6):
    raise RuntimeError("Only Python 3.6+ is supported.")

def get_base_path():
    return path.split(path.realpath(__file__))[0]

def getConfig(section, key):
    config = configparser.ConfigParser()
    config.read(path.join(get_base_path(), 'app.ini'))
    return config.get(section, key)

if not path.exists(path.join(get_base_path(), getConfig('sqlite', 'File'))):
    db = get_db()
    with open(path.join(get_base_path(), 'schema.sql'), 'r') as f:
        try:
            with db:
                db.executescript(f.read())
        except sqlite3.OperationalError as e:
            print("init db error:", e)
        finally:
            close_db(db)
