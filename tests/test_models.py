import os
from os.path import join, exists
import shutil
import tempfile

import git
import pytest

from mini_wiki.models import Page, PageError, ParseError, NoRenderEngineError
from mini_wiki.utils import filename_to_title



@pytest.fixture
def git_repo(request):
    temp_dir = tempfile.mkdtemp()
    git_repo = git.Repo.init(temp_dir)
    request.addfinalizer(lambda temp_dir=temp_dir: shutil.rmtree(temp_dir))
    return git_repo


@pytest.fixture
def page(git_repo):
    filename = join(git_repo.working_tree_dir, 'a_dummy_file.txt')
    content = "This is just a random file"
    
    return Page(filename=filename, 
                content=content, 
                repo=git_repo)


def test_git_repo(git_repo):
    assert exists(git_repo.working_tree_dir)

def test_page(page):
    assert exists(page.repo.working_tree_dir)


class TestPage:
    def test_init_no_config(self):
        _, filename = tempfile.mkstemp(suffix='.md')
        title = filename_to_title(filename)
        content = "This is just a random file"
        
        p = Page(filename=filename, content=content)

        assert p.config['title'] == title
        assert p.filename == filename
        assert p.content == content
        assert p.title == title

        os.remove(filename)
        assert not exists(filename)

    def test_init_with_config(self):
        _, filename = tempfile.mkstemp(suffix='.md')
        title = filename_to_title(filename)
        content = "This is just a random file"
        config = {'extra': 'blah'}
        
        p = Page(filename=filename, content=content, config=config)

        assert p.config['title'] == title
        assert p.config == config
        assert p.filename == filename
        assert p.content == content

        os.remove(filename)
        assert not exists(filename)

    def test_init_with_title_in_config(self):
        _, filename = tempfile.mkstemp()
        content = "This is just a random file"
        config = {'title': 'blah'}
        
        with pytest.raises(ValueError):
            p = Page(filename=filename, content=content, config=config)

        os.remove(filename)
        assert not exists(filename)

    def test_head(self, page):
        assert page.config == {'title': 'A Dummy File'}
        should_be = '\n'.join([
                '---',
                'title: A Dummy File',
                '---'
                ])
        assert page.header() == should_be

    def test_format(self, page):
        assert page.content == "This is just a random file"
        assert page.config == {'title': 'A Dummy File'}

        should_be = '\n'.join([
                '---',
                'title: A Dummy File',
                '---',
                '',
                'This is just a random file'])
        assert page.format() == should_be

    def test_save_valid(self, page):
        assert not exists(page.filename)
        page.save()
        assert exists(page.filename)
        assert open(page.filename).read() == page.format()

        # Make sure we staged the file
        paths = [path for (path, stage), entry 
                in page.repo.index.entries.items()]

        relative_filename = page.filename.replace(
                page.repo.working_tree_dir + os.path.sep, 
                '')
        assert relative_filename in paths

    def test_save_no_filename(self, page):
        page.filename = None
        with pytest.raises(PageError):
            page.save()

    def test_save_no_repo(self, page):
        page.repo = None
        with pytest.raises(PageError):
            page.save()

    def test_commit(self, page):
        author = git.Actor('John Smith', 'john@example.org')
        page.commit('did some stuff', author=author)
        assert not page.repo.is_dirty()

    def test_str(self, page):
        assert str(page) == page.format()

    def test_from_file_FileNotFound(self):
        with pytest.raises(FileNotFoundError):
            some_page = Page.from_file('non/existent/file.md')

    def test_from_file_invalid_file(self):
        src = """
        ---
        title: A Dummy File

        ---

        Woops, did I accidentally put a newline in the header?
        """.strip()

        _, filename = tempfile.mkstemp()
        open(filename, 'w').write(src)
        assert os.path.exists(filename)

        with pytest.raises(ParseError):
            some_page = Page.from_file(filename)

        os.remove(filename)
        assert not exists(filename)

    def test_from_file_valid(self):
        _, filename = tempfile.mkstemp()
        title = filename_to_title(filename)

        src = """
        ---
        title: {}
        ---

        The body of some file
        """.format(title).strip()

        open(filename, 'w').write(src)
        assert os.path.exists(filename)

        some_page = Page.from_file(filename)

        assert some_page.config == {'title': title}
        assert some_page.content == 'The body of some file'

        os.remove(filename)
        assert not exists(filename)

    def test_to_html_no_markup_specified(self):
        filename = 'blah'
        content = 'This is just a random file'
        page = Page(filename=filename, content=content)
        should_be = '<p>This is just a random file</p>'
        assert page.to_html() == should_be

    def test_to_html_html_format(self):
        filename = 'blah'
        content = 'This is just a random file'
        config = {'format': 'html'}
        page = Page(filename=filename, config=config, content=content)
        should_be = 'This is just a random file'
        assert page.to_html() == should_be

    def test_to_html_unknown_format(self):
        filename = 'blah'
        content = 'This is just a random file'
        config = {'format': 'pdf'}
        page = Page(filename=filename, config=config, content=content)
        should_be = 'This is just a random file'
        with pytest.raises(NoRenderEngineError):
            page.to_html()

    def test_to_html(self, page):
        should_be = '<p>This is just a random file</p>'
        assert page.to_html() == should_be


class TestParser:
    def test_parse_valid(self):
        src = """
        ---
        title: Blah
        ---

        This is the body.
        """.strip()
        header, body = Page.parse_text(src)
        assert header == {'title': 'Blah'}
        assert body == 'This is the body.'

    def test_parse_no_starting_dash(self):
        src = """
        title: Blah
        ---

        This is the body.
        """.strip()
        with pytest.raises(ParseError):
            header, body = Page.parse_text(src)

    def test_parse_no_ending_dash(self):
        src = """
        ---
        title: Blah

        This is the body.
        """.strip()
        with pytest.raises(ParseError):
            header, body = Page.parse_text(src)

    def test_parse_newline_in_header(self):
        src = """
        ---
        title: Blah

        ---

        This is the body.
        """.strip()
        with pytest.raises(ParseError):
            header, body = Page.parse_text(src)

    def test_parse_no_newline_after_header(self):
        src = """
        ---
        title: Blah
        ---
        This is the body.
        """.strip()
        with pytest.raises(ParseError):
            header, body = Page.parse_text(src)

