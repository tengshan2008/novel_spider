import argparse
import sys
import time

from . import crawel
from .config import HOST


def cmd():
    description = "caoliu(t66y) crawl novel program "
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-s", "--start", type=int, default=1,
                        help="what page you what start")
    parser.add_argument("-e", "--end", type=int,
                        help="what page you what end")
    parser.add_argument("-l", "--loop", action="store_true",
                        help="is loop crawl")
    parser.add_argument("-d", "--desc", action="store_true",
                        help="is sort desc")
    args = parser.parse_args()

    if args.loop:
        while True:
            crawl_with_start_end(args.start, args.end, args.desc)
            time.sleep(12 * 60 * 60)
    else:
        crawl_with_start_end(args.start, args.end, args.desc)


def crawl_with_start_end(start, end, sort_desc):
    url = f"{HOST}/thread0806.php?fid=20&search=&page=1"
    crawl = crawel.Crawl(url, start, end, sort_desc)
    crawl.start()


if __name__ == "__main__":
    cmd()
