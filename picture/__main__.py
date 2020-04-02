import argparse
from multiprocessing import Process

from daemon import runner

from . import check, db, gif
from .config import DB_FILE


class App(object):
    def __init__(self, url):
        self.url = url
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/tmp/picture_error.log'
        self.pidfile_path = '/tmp/picture.pid'
        self.pidfile_timeout = 5

    def run(self):
        database = db.Database(DB_FILE)
        database.init()
        page = gif.Page(self.url)
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

    app = App(args.link)

    if args.check:
        check.check_all()
        return
    if args.daemon:
        daemon_runner = runner.DaemonRunner(app)
        daemon_runner.do_action()
        return

    app.run()


if __name__ == "__main__":
    cmd()
