from argparse import ArgumentParser

from pathlib import Path
from daemon import DaemonContext

from . import check, db, gif, logger
from .config import DB_FILE


def run(url):
    logger.add(Path(__file__).parent / 'output.log',
               colorize=True, encoding='utf-8')
    database = db.Database(DB_FILE)
    database.init()
    page = gif.Page(url)
    if page.parse() is None:
        return
    page.download()


def cmd():
    description = 'caoliu(t66y) crawl picture program '
    parser = ArgumentParser(description=description)
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
        errlog = Path(__file__).parent / "err.log"
        with DaemonContext(stderr=errlog.open("w")):
            run(args.link)
        return

    run(args.link)


if __name__ == "__main__":
    cmd()
