import configparser
from os import path

base_path = path.split(path.realpath(__file__))[0]

def get(section, key):
    config = configparser.ConfigParser()
    config.read(path.join(base_path, 'app.ini'))
    return config.get(section, key)
