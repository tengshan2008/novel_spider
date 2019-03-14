import configparser
from os import path

base_path = path.split(path.realpath(__file__))[0]

def _get_config():
    config = configparser.ConfigParser()
    config.read(path.join(base_path, 'app.ini'))
    return config

def get(section, key):
    return _get_config().get(section, key)

def getboolean(section, key):
    return _get_config().getboolean(section, key)
