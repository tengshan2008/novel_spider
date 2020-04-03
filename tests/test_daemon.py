import time
from argparse import ArgumentParser
from daemon import DaemonContext
import sys


class App():
    def __init__(self, text):
        self.text = text
        # self.stdin_path = '/dev/null'
        # self.stdout_path = '/dev/tty'
        # self.stderr_path = '/dev/tty'
        # self.pidfile_path = '/tmp/foo.pid'
        # self.pidfile_timeout = 5

    def run(self):
        while True:
            with open('/tmp/output.log', 'a') as f:
                f.write(self.text + "\n")
            time.sleep(1)


def cmd():
    parser = ArgumentParser()
    parser.add_argument("-t", "--test", type=str,
                        help="input test text")
    # parser.add_argument("-d", "--daemon", action="store_true",
    #                     help="daemon mode")
    argvs = sys.argv
    print(argvs)
    if "start" in sys.argv:
        argvs.remove("start")
    print(argvs)
    args = parser.parse_args(argvs[1:])

    text = "Howdy!  Gig'em!  Whoop!"
    if args.test is not None:
        text = args.test
    app = App(text)

    with DaemonContext():
        app.run()


if __name__ == "__main__":
    cmd()
