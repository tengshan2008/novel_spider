import time
import argparse
from multiprocessing import Process


def run(name):
    time.sleep(1)
    print('hello', name)
    print('我是子进程')


def cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--daemon", action="store_true",
                        help="daemon mode")
    args = parser.parse_args()

    if args.daemon:
        backend('bob')
        return

    print("no daemon")


def backend(name):
    p = Process(target=run, args=(name,))
    p.start()


if __name__ == '__main__':
    cmd()
