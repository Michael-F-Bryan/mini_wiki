#!/usr/bin/env python3
""" A top level management script to start the application and do various admin tasks.
"""

import os
from mini_wiki import create_app, db
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

from config import config


profile = config[os.environ.get('FLASK_CONFIG') or 'default']
app = create_app(profile)
manager = Manager(app)
migrate = Migrate(app, db)


manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()


