from datetime import datetime
from flask import (render_template, session, redirect, url_for, request, 
        flash, request)
from flask.ext.login import current_user 

from . import main
from .. import db
from ..models import User 


@main.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html')



