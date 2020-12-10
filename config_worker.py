import json
import os
import pathlib

CONFIG_PATH = pathlib.Path(os.path.join(os.path.abspath(os.curdir), "config.json"))


def load_config():
    try:
        config = json.load(open(CONFIG_PATH))
    except Exception:
        config = {
            "lang": "RU",
        }
        file = open(CONFIG_PATH, mode='w')
        file.write(json.dumps(config))
        file.close()
    return config


def write_config(*args, **kwargs):
    pass


def get_lang():
    return load_config()['lang']
