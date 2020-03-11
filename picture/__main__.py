import argparse

from . import gif


def cmd():
    parser = argparse.ArgumentParser(description='caoliu(t66y) crawl picture program ')
    parser.add_argument("-l", "--link", type=str,
                        help="blog link of picture")
    args = parser.parse_args()
    gif.get_gif(url)


if __name__ == "__main__":
    cmd()
