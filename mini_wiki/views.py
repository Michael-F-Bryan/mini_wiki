from flask import Blueprint, render_template, abort
from .utils import valid_page
from .models import Page, ParseError


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
    page_path = valid_page(page_path)
    if not page_path:
        abort(404)

    try:
        page = Page.from_file(page_path)
    except ParseError as e:
        # The page has been formatted incorrectly
        abort(500)

    return render_template('page.html', 
            page_title=page.title,
            page_content=page.to_html())

