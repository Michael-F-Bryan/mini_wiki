import os 
from flask import current_app
from .models import Page, PageError



def dict_keys_to_upper(some_dict):
    return {key.upper():value for key, value in some_dict.items()}


def valid_page(path):
    return _valid_page(path) or _valid_page(path + '/index.md')

def _valid_page(path):
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

    if os.path.isdir(destination):
        return False

    return destination

def filename_to_title(filename):
    """
    Turn a filename from a normal path to it's equivalent title. This usually
    involves the following changes:
    - replacing all underscores with spaces
    - removing the extension
    - making it titlecase
    """
    filename = os.path.basename(filename)
    title, file_extension = os.path.splitext(filename)
    title = title.replace('_', ' ')
    title = title.title()
    return title

def title_to_filename(title, parent_dir='', ext='md'):
    """
    Turn a file's title into it's equivalent filename.

    This usually involves:
    - replace all spaces with underscores
    - make everything lowercase
    - prepend the filename with it's parent directory
    - add the appropriate extension

    Raises
    ------
    ValueError
        If the filename contains a forward slash ("/")
    """
    if '/' in title:
        raise ValueError("Titles can't contain '/'")
    filename = title.replace(' ', '_')
    filename = filename.lower()
    return os.path.join(parent_dir, filename + '.' + ext)


class TreeNode:
    def __init__(self, path, base_path):
        self.path = path
        self.children = []
        self.base_path = base_path
        

    def add_child(self, child_node):
        self.children.append(child_node)

    def name(self):
        return filename_to_title(self.path)

    def __repr__(self):
        return '<{}: path="{}" children={}>'.format(
                self.__class__.__name__,
                self.path,
                len(self.children))

    def is_index(self):
        return os.path.basename(self.path) == 'index.md'

    def location(self):
        """
        Get the location relative to the _site directory
        """
        href = self.path.replace(self.base_path, '')
        if href.startswith('/'):
            href = href[1:]
        if os.path.basename(href) == 'index.md':
            href = os.path.dirname(href)
        return href


def tree(root_dir):
    root_node = TreeNode(root_dir, root_dir)
    add_children(root_node, root_dir, root_dir)
    return root_node


def add_children(parent_node, path, base_path):
    for thing in os.listdir(path):
        child_path = os.path.join(path, thing)
        new_node = TreeNode(child_path, base_path)
        parent_node.add_child(new_node)

        if os.path.isdir(child_path):
            add_children(new_node, child_path, base_path)
    
