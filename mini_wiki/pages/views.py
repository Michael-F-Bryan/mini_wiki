import os
from datetime import datetime
from flask import (render_template, session, redirect, url_for, request, 
        flash, request, current_app, abort)
from flask.ext.login import current_user 

from . import pages
from .misc import read_front_matter, ParseError
from .. import db
from ..models import User 


@pages.route('/', defaults={'path': ''})
@pages.route('/<path:path>', methods=['GET'])
def homepage(path):
    filename = os.path.join(current_app.config['SITE_ROOT'], path)
    filename = verify_filename(filename)

    if filename:
        page = read_front_matter(filename)
        return render_template('page.html',page=page)
    else:
        abort(404)


def verify_filename(filename):
    if not filename.startswith(current_app.config['SITE_ROOT']):
        # They're trying to do something sneaky like /pages/../../../etc/fstab
        return False

    for ext in current_app.config['VALID_EXTENSIONS']:
        if os.path.exists(filename + ext):
            return filename + ext
    return False
