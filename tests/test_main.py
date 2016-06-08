import os
import tempfile
import pytest
from flask import url_for, current_app
from mini_wiki.models import Page


class TestViews:
    def test_homepage(self, client):
        client.get(url_for('main.homepage'))

    def test_404(self, client):
        client.get('iuewsdfhuiwcfhbewdcewf')

    # def test_500(self, client):
    #     client.get(url_for('server_error'))

    def test_wiki_page_404(self, client):
        filename = 'some/random/file'
        assert not os.path.exists(filename)
        r = client.get(url_for('main.wiki_page', page_path=filename))
        assert r.status_code == 404

    def test_wiki_page_valid(self, client):
        src = """
        ---
        title: A Dummy File
        ---

        The body of some file
        """.strip()
        headers, body = Page.parse_text(src)

        site_folder = os.path.join(current_app.config['WIKI_DIR'], '_site')
        _, temporary_file = tempfile.mkstemp(dir=site_folder, suffix='.txt')
        open(temporary_file, 'w').write(src)
        assert os.path.exists(temporary_file)

        relative_filename = temporary_file.replace(site_folder, '')
        relative_filename = relative_filename[1:]

        url = url_for('main.wiki_page', page_path=relative_filename)
        r = client.get(url)
        assert r.status_code == 200

        assert body in r.get_data(as_text=True)

        os.remove(temporary_file)
        assert not os.path.exists(temporary_file)

    def test_wiki_page_parse_error(self, client):
        src = """
        title: A Dummy File
        ---

        The body of some file
        """.strip()

        site_folder = os.path.join(current_app.config['WIKI_DIR'], '_site')
        _, temporary_file = tempfile.mkstemp(dir=site_folder, suffix='.txt')
        open(temporary_file, 'w').write(src)
        assert os.path.exists(temporary_file)

        relative_filename = temporary_file.replace(site_folder, '')
        relative_filename = relative_filename[1:]

        url = url_for('main.wiki_page', page_path=relative_filename)
        r = client.get(url)
        assert r.status_code == 500

        os.remove(temporary_file)
        assert not os.path.exists(temporary_file)
