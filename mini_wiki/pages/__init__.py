from flask import Blueprint, render_template

pages = Blueprint('pages', __name__)

from . import views

