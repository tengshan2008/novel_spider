import argparse

from . import db, gif
from .config import DB_FILE


def cmd():
    description = 'caoliu(t66y) crawl picture program '
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-l", "--link", type=str,
                        help="blog link of picture")
    args = parser.parse_args()

    database = db.Database(DB_FILE)
    database.init()
    page = gif.Page(args.link)
    page.parse()
    page.download()


if __name__ == "__main__":
    cmd()
