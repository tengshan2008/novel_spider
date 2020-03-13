import argparse
import sys

from . import crawel
from .config import HOST


def cmd():
    description = "caoliu(t66y) crawl novel program "
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-s", "--start", type=int, default=1,
                        help="what page you what start")
    parser.add_argument("-e", "--end", type=int,
                        help="what page you what end")
    parser.add_argument("-l", "--loop", type=bool,
                        help="is loop crawl")
    args = parser.parse_args()

    crawl_with_start_end(args.start, args.end)


def crawl_with_start_end(start, end):
    url = f"{HOST}/thread0806.php?fid=20&search=&page=1"
    crawl = crawel.Crawl(url, start, end)
    crawl.start()


if __name__ == "__main__":
    cmd()
