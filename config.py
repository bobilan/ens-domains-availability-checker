#!/usr/bin/python
import os
from configparser import SafeConfigParser


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = SafeConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            param_name = param[0]
            if param_name != "database":
                value = os.environ[param[1]]
            else:
                value = param[1]
            db[param_name] = value
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return db


DB_CONFIG = config()
