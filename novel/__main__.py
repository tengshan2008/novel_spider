from . import crawel
from . import host
import sys
import argparse


def cmd():
    parser = argparse.ArgumentParser(description="caoliu(t66y) crawl program ")
    parser.add_argument("-s", "--start", type=int, default=1,
                        help="what page you what start")
    args = parser.parse_args()

    url = f"{host}/thread0806.php?fid=20&search=&page=1"
    crawl = crawel.Crawl(url, args.start)
    crawl.start()


if __name__ == "__main__":
    cmd()
