import os
from flask import Blueprint, render_template, abort, current_app
from .utils import valid_page, tree
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


@main.route('/wiki/', methods=['GET'])
def wiki_index():
    root_dir = os.path.join(current_app.config['WIKI_DIR'], '_site')
    root_node = tree(root_dir)

    return render_template('page_index.html', root_node=root_node)


@main.route('/wiki/<path:page_path>', methods=['GET'])
def wiki_page(page_path):
    """
    Get the file located at `page_path` and render it as a html page.
    """
    # Make sure the page exists
    page_path = valid_page(page_path)
    print(page_path)
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

