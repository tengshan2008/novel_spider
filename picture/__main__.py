import argparse

from . import gif


def cmd():
    description = 'caoliu(t66y) crawl picture program '
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-l", "--link", type=str,
                        help="blog link of picture")
    args = parser.parse_args()
    gif.get_gif(args.link)


if __name__ == "__main__":
    cmd()
