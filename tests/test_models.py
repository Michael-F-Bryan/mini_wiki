import os
from os.path import join, exists
import shutil
import tempfile

import git
import pytest

from mini_wiki.models import Page, PageError



@pytest.fixture
def git_repo(request):
    temp_dir = tempfile.mkdtemp()
    git_repo = git.Repo.init(temp_dir)
    request.addfinalizer(lambda temp_dir=temp_dir: shutil.rmtree(temp_dir))
    return git_repo


@pytest.fixture
def page(git_repo):
    filename = join(git_repo.working_tree_dir, 'some_file.txt')
    title = 'A Dummy File'
    content = "This is just a random file"
    
    return Page(filename=filename, 
                content=content, 
                title=title, 
                repo=git_repo)


def test_git_repo(git_repo):
    assert exists(git_repo.working_tree_dir)

def test_page(page):
    assert exists(page.repo.working_tree_dir)



class TestPage:
    def test_init(self):
        _, filename = tempfile.mkstemp()
        title = 'A Dummy File'
        content = "This is just a random file"
        
        p = Page(filename=filename, content=content, title=title)

        assert p.config['title'] == title
        assert p.filename == filename
        assert p.content == content

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
