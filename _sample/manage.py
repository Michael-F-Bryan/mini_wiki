#!/usr/bin/env python3
""" A top level management script to start the application and do various admin tasks.
"""

import os
import warnings
import argparse
from yaml import load
from mini_wiki import create_app, db


project_dir = os.path.abspath(os.path.dirname(__file__))
config_file = os.path.join(project_dir, 'config.yml')

conf = {
    'secret_key': 'my super secret key',
    'sqlalchemy_commit_on_teardown': True,
    'sqlalchemy_track_modifications': False,
    'allow_registration': os.environ.get('ALLOW_REGISTRATION') or True,
    'template_dir': os.path.join(project_dir, 'templates'),
    'site_root': os.path.join(project_dir, '_site'),
    'valid_extensions': ['.md'],
    'debug': True,
    'log_file': os.path.join(project_dir, 'mini_wiki.log'),
        }

try:
    from_config = load(open(config_file).read())
    conf.update(from_config)
except FileNotFoundError:
    # Couldn't find the config file
    warning.warn('Configuration file not found inside root directory')

conf = {key.upper(): value for key, value in conf.items()}

app = create_app(conf)

def run(**kwargs):
    app.run(port=kwargs['port'], host=kwargs['host'])


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=None)
    subparsers = parser.add_subparsers(help='sub-command help')

    # Create a parser for the "run" command
    run_parser = subparsers.add_parser('run', help='Run the dev server')
    run_parser.add_argument('-p', '--port', dest='port', type=int, default=5000,
            help='The port for the dev server to run on')
    run_parser.add_argument('-H', '--host', dest='host', default='127.0.0.1',
            help='The host for the dev server to run on')
    run_parser.set_defaults(func=run)

    args = parser.parse_args()

    if args.func:
        args.func(**args.__dict__)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()


