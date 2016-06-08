from flask import render_template
from . import main


@main.app_errorhandler(404)
def four_oh_four(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@main.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html')
