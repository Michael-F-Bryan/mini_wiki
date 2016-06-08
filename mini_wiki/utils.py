import os 
from flask import current_app
from .models import Page, PageError



def dict_keys_to_upper(some_dict):
    return {key.upper():value for key, value in some_dict.items()}


def valid_page(path):
    """
    Check if a file exists and is within the _site folder.
    """
    # Remove a leading '/' if present
    if path.startswith('/'):
        path = path[1:]

    site_folder = os.path.join(current_app.config['WIKI_DIR'], '_site')
    destination = os.path.join(site_folder, path)

    if '../' in path:
        # They're trying to access something outside the _site folder
        return False

    if not os.path.exists(destination):
        return False

    return destination

