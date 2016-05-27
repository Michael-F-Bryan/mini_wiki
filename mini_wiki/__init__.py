from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import jinja2

# Versioneer
from ._version import get_versions
_version = get_versions()['version']
__version__ = _version.split('+')[0]
del get_versions


bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(conf):
    """
    A factory function for creating Flask apps given a configuration 
    dictionary.

    The factory will initialise all Flask plugins, as well as change the 
    template directory and load all blueprints.

    The factory function also sets up logging and adds the `wiki` variable
    to the template globals.
    """
    app = Flask(__name__)
    app.config.update(conf)

    # Tell flask to get all templates from our template dir
    my_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(conf['TEMPLATE_DIR']),
    ])
    app.jinja_loader = my_loader

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    
    # Attach routes and custom error pages
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .pages import pages as pages_blueprint
    app.register_blueprint(pages_blueprint, url_prefix='/pages')

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

    # Inject the app metadata into all our templates
    app.jinja_env.globals['wiki'] = conf['METADATA']

    return app

