from flask import Blueprint, render_template, abort
from .utils import valid_page


main = Blueprint('main', __name__)


@main.app_errorhandler(404)
def four_oh_four(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@main.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html')


@main.route('/wiki/<path:page_path>', methods=['GET'])
def wiki_page(page_path):
    # Make sure the page exists
    if not valid_page(page_path):
        abort(404)
