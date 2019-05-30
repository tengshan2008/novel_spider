import random
from os import path

base_path = path.split(path.realpath(__file__))[0]


def get_all():
    pool = []
    with open(path.join(base_path, 'pool.txt'), 'r') as f:
        for line in f.readlines():
            pool.append(line.strip())
    return pool


def get_random():
    return random.choice(get_all())

# https://www.xicidaili.com/
# http://www.gatherproxy.com/zh/
