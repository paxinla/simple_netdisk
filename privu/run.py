#!/usr/bin/env python
#coding=utf-8

import sys
import os
import argparse

import simplejson as json

from privu.core import app, setup_app_config


def parse_input():
    parser = argparse.ArgumentParser(description="Personal simple temporary netdisk.",
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("--conf", dest="conf_file", type=str, required=True,
                        help="Configuration file in json format is needed.")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    parsed_args = parser.parse_args()
    return vars(parsed_args)


def main():
    conf_json = parse_input().get("conf_file", None)
    conf = {}

    if conf_json is None or (not os.path.exists(conf_json)):
        raise ValueError(f"Expected json {conf_json} not found !")
        sys.exit(1)

    with open(conf_json, 'r', encoding='utf8') as rf:
        conf = json.loads(rf.read())

    setup_app_config(conf)
    app.run(host=conf.get("host", '127.0.0.1'),
            port=conf.get("port", 8080))


if __name__ == "__main__":
    main()
