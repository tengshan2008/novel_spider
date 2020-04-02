import argparse
from multiprocessing import Process

from . import db, gif, check
from .config import DB_FILE


def run(url):
    database = db.Database(DB_FILE)
    database.init()
    page = gif.Page(url)
    page.parse()
    page.download()


def cmd():
    description = 'caoliu(t66y) crawl picture program '
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-l", "--link", type=str,
                        help="blog link of picture")
    parser.add_argument("-c", "--check", action="store_true",
                        help="check miss picture")
    parser.add_argument("-d", "--daemon", action="store_true",
                        help="daemon mode")
    args = parser.parse_args()

    if args.check:
        check.check_all()
        return
    if args.daemon:
        backend(args.link)
        return

    run(args.link)


def backend(url):
    p = Process(target=run, args=(url,))
    p.daemon = True
    p.start()


if __name__ == "__main__":
    cmd()
