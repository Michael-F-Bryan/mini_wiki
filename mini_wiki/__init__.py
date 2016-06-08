from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .utils import dict_keys_to_upper
from ._version import get_versions
__version__ = get_versions()['version'].split('+')[0]


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

default_settings = {
        'debug': False,
        'testing': False,
        'secret_key': 'some-super-secret-key-that-should-probably-be-changed',
        'logger_handler_policy': 'always',
        'sqlalchemy_track_modifications': False,
        }
default_settings = dict_keys_to_upper(default_settings)  # Make keys upper case

def create_app(config_dict, wiki_dir=None):
    config_dict = dict_keys_to_upper(config_dict)

    app = Flask(__name__)
    app.config.update(default_settings)
    app.config.update(config_dict)
    app.config['wiki_dir'] = wiki_dir

    db.init_app(app)
    login_manager.init_app(app)
    
    # Attach routes and custom error pages
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    if app.config.get('LOG_FILE'):
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
                app.config.get('LOG_FILE'), 
                maxBytes=1024 * 1024 * 100, 
                backupCount=20)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s: %(message)s",
                datefmt='%Y/%m/%d %I:%M:%S %p')
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

        # Catch the requests behind the scenes from werkzeug
        logger = logging.getLogger('werkzeug')
        logger.addHandler(file_handler)

    return app

