import argparse

from . import gif


def cmd():
    description = 'caoliu(t66y) crawl picture program '
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-l", "--link", type=str,
                        help="blog link of picture")
    args = parser.parse_args()
    page = gif.Page(args.link)
    page.download()


if __name__ == "__main__":
    cmd()
