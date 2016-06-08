from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from ._version import get_versions

__version__ = get_versions()['version'].split('+')[0]

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    login_manager.init_app(app)
    
    # Attach routes and custom error pages
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

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


