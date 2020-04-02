import argparse

from . import check, db, gif
from .config import DB_FILE


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
        # daemon_runner = runner.DaemonRunner(app)
        # daemon_runner.do_action()
        return

    database = db.Database(DB_FILE)
    database.init()
    page = gif.Page(args.link)
    page.parse()
    page.download()


if __name__ == "__main__":
    cmd()
