import sqlite3
import os

from banzhu import logger
from util import config

base_path = os.path.split(os.path.realpath(__file__))[0]

sql_read = """
    SELECT size
    FROM novel
    WHERE nid = ?
"""

sql_insert = """
    INSERT
    INTO novel(nid, title, author, ndate, link, size)
    VALUES (?, ?, ?, ?, ?, ?)
"""

sql_update = """
    UPDATE novel
    SET size = ?
    WHERE nid = ?
"""

sql_delete = """
    DELETE
    FROM novel
    WHERE nid = ?
"""

def get()