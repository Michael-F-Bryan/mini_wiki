#!/usr/bin/env python3
""" A top level management script to start the application and do various admin tasks.
"""

import os
from mini_wiki import create_app, db
import yaml
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


wiki_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(wiki_dir, 'config.yml')

# Load our config settings
if os.path.exists(config_file):
    config = yaml.load(open(config_file).read())
else:
    # Use the default settings
    config = {}

if 'template_dir' not in config:
    config['template_dir'] = os.path.join(wiki_dir, 'templates')

config['wiki_dir'] = wiki_dir

app = create_app(config)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
