import os
import tempfile
from flask import current_app
import pytest
from mini_wiki import utils


class TestValidPath:
    def test_doesnt_exist(self, client):
        filename = 'non/existent/file.txt'
        assert not os.path.exists(filename)
        assert not utils.valid_page(filename)

    def test_dot_dot(self, client):
        filename = '/../../../../../../../etc/passwd'
        assert not utils.valid_page(filename)
        filename = '../../../../../../../etc/passwd'
        assert not utils.valid_page(filename)

    def test_existing_file(self, client):
        site_folder = os.path.join(current_app.config['WIKI_DIR'], '_site')
        _, temporary_file = tempfile.mkstemp(dir=site_folder, suffix='.txt')
        assert os.path.exists(temporary_file)

        file_path = temporary_file.replace(site_folder, '')
        assert utils.valid_page(file_path) == temporary_file

        os.remove(temporary_file)
        assert not os.path.exists(temporary_file), "The temp file wasn't deleted"

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
