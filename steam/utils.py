import os
import json
import logging

config_path = 'cfg'

def dir_check(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)


def load_config_file(config_file):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except IOError:
        logging.warning('{} not found.'.format(config_file))
        config = {}
    return config
