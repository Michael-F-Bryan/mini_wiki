import os
import tempfile
from flask import current_app
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

