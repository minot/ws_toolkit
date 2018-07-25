# -*- coding: utf-8 -*-

import yaml
import os


def config():
    file_path = os.path.split(os.path.realpath(__file__))[0]
    config_path = os.path.join(file_path, 'config.yaml')
    config_file = open(config_path, 'r', encoding='UTF-8')
    cont = config_file.read()

    conf = yaml.load(cont)

    return conf
