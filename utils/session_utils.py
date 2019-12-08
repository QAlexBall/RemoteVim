import os
import json

def read_config(config_path=None):
    if config_path is None:
        config_path = os.path.abspath(os.path.dirname(__file__)) + "/config.json"
    config_file = open(config_path, 'r')
    config = json.load(config_file)
    config_file.close()
    return config


def change_current_path():
    pass


def write_config(config, config_path=None):
    if config_path is None:
        config_path = os.path.abspath(os.path.dirname(__file__)) + "/config.json"
    config_file = open(config_path, 'w')
    json.dump(config, config_file, indent=4)
    config_file.close()