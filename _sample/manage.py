#!/usr/bin/env python3
""" A top level management script to start the application and do various admin tasks.
"""

import os
import warnings
import argparse
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from yaml import load
from mini_wiki import create_app, db


project_dir = os.path.abspath(os.path.dirname(__file__))
config_file = os.path.join(project_dir, 'config.yml')

# These are the defaults that we use for the server
conf = {
    'secret_key': 'my super secret key',
    'sqlalchemy_commit_on_teardown': True,
    'sqlalchemy_track_modifications': False,
    'allow_registration': os.environ.get('ALLOW_REGISTRATION') or True,
    'template_dir': os.path.join(project_dir, 'templates'),
    'site_root': os.path.join(project_dir, '_site'),
    'valid_extensions': ['.md'],
    'debug': False,
    'log_file': os.path.join(project_dir, 'mini_wiki.log'),

    'metadata': {
        'website_name': 'My Awesome Wiki',
        'admin_email': 'admin@example.com',
        },
}

try:
    from_config = load(open(config_file).read())
    conf.update(from_config)
except FileNotFoundError:
    # Couldn't find the config file
    warning.warn('Configuration file not found inside root directory')

conf = {key.upper(): value for key, value in conf.items()}
app = create_app(conf)

# Initialize flask-manage and flask-migrate
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()


