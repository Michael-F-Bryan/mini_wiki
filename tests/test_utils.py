import os
import shutil
import tempfile
from flask import current_app
import pytest
from mini_wiki import utils


class TestValidPath:
    def test_valid_page_same_as_underscore(self, client):
        filename = 'non/existent/file.txt'
        assert not os.path.exists(filename)
        assert utils._valid_page(filename) == utils.valid_page(filename)

    def test_doesnt_exist(self, client):
        filename = 'non/existent/file.txt'
        assert not os.path.exists(filename)
        assert not utils._valid_page(filename)

    def test_dot_dot(self, client):
        filename = '/../../../../../../../etc/passwd'
        assert not utils.valid_page(filename)
        filename = '../../../../../../../etc/passwd'
        assert not utils._valid_page(filename)

    def test_existing_file(self, client):
        site_folder = os.path.join(current_app.config['WIKI_DIR'], '_site')
        _, temporary_file = tempfile.mkstemp(dir=site_folder, suffix='.txt')
        assert os.path.exists(temporary_file)

        file_path = temporary_file.replace(site_folder, '')
        assert utils._valid_page(file_path) == temporary_file

        os.remove(temporary_file)
        assert not os.path.exists(temporary_file), "The temp file wasn't deleted"

    def test_folder_with_index_md(self, client):
        site_folder = os.path.join(current_app.config['WIKI_DIR'], '_site')
        temporary_folder = tempfile.mkdtemp(dir=site_folder, suffix='.txt')
        assert os.path.exists(temporary_folder)

        # Make an "index.md" file inside the temp folder
        temp_index = os.path.join(temporary_folder, 'index.md')
        open(temp_index, 'w').write('')
        assert os.path.exists(temp_index)

        file_path = temporary_folder.replace(site_folder, '')

        assert utils.valid_page(file_path) == temp_index

        shutil.rmtree(temporary_folder)
        assert not os.path.exists(temporary_folder), "The temp file wasn't deleted"

class TestFilenameToTitle:
    def test_basic(self):
        some_filename = 'Path/to/some_file.txt'
        should_be = 'Some File'
        assert utils.filename_to_title(some_filename) == should_be

    def test_with_hyphen_and_dot(self):
        some_filename = 'Path/to/some_file-version-123.bak.txt'
        should_be = 'Some File-Version-123.Bak'
        assert utils.filename_to_title(some_filename) == should_be

class TestTitleToFilename:
    def test_basic(self):
        title = 'Blah'
        ext = 'md'
        parent_dir = '/home/michael'
        should_be = '/home/michael/blah.md'
        assert utils.title_to_filename(title, parent_dir, ext) == should_be

    def test_with_slash(self):
        with pytest.raises(ValueError):
            utils.title_to_filename('Some Title 19/5/2016')

    def test_multiple_words(self):
        title = 'This Is A Title - V1'
        ext = 'md'
        parent_dir = '/home/michael'
        should_be = '/home/michael/this_is_a_title_-_v1.md'
        assert utils.title_to_filename(title, parent_dir, ext) == should_be


@pytest.fixture
def node(request):
        temporary_folder = tempfile.mkdtemp()
        assert os.path.exists(temporary_folder)

        # Make an "index.md" file inside the temp folder
        temp_index = os.path.join(temporary_folder, 'index.md')
        open(temp_index, 'w').write('')
        assert os.path.exists(temp_index)

        node = utils.TreeNode(temp_index, temporary_folder)

        request.addfinalizer(lambda : shutil.rmtree(temporary_folder))
        return node


class TestTreeNode:
    def test_init(self):
        _, temporary_file = tempfile.mkstemp(suffix='.txt')
        assert os.path.exists(temporary_file)

        node = utils.TreeNode(temporary_file, temporary_file)

        assert node.path == temporary_file
        assert node.base_path == temporary_file
        assert node.children == []

        os.remove(temporary_file)
        assert not os.path.exists(temporary_file)

    def test_add_child(self, node):
        dummy_node = utils.TreeNode('some_filname', 'some_path')
        assert node.children == []
        node.add_child(dummy_node)
        assert node.children == [dummy_node]

    def test_is_index(self, node):
        assert node.is_index()

    def test_name(self, node):
        assert node.name() == utils.filename_to_title(node.path)

    def test_location_for_index_md(self, node):
        # The node is the index.md child of the base_name
        # Therefore when replacing the base_name and then removing "index.md"
        # You are left with nothing
        # So technically this file shouldn't exist
        assert node.location() == ''

    def test_location_basic(self):
        base_path = '/_site'
        node_path = '/_site/path/to/file.md'
        some_node = utils.TreeNode(node_path, base_path)
        assert some_node.location() == 'path/to/file.md'

