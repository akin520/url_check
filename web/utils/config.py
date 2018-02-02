#!/usr/bin/env python

import yaml

# configure
CONFIG = None


def load_config():
    global CONFIG
    with open("cfg.yaml", "rb") as f:
        CONFIG = yaml.load(f)
