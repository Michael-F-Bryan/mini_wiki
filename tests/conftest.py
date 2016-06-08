import os
import pytest
from mini_wiki import create_app 


@pytest.fixture
def app(request):
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_dir = os.path.join(project_dir, '_sample')
    template_dir = os.path.join(sample_dir, 'templates')

    testing_config = {
            'template_dir': template_dir,
            'server_name': 'localhost',
            'wiki_dir': sample_dir,
            }

    test_client = create_app(testing_config)
    return test_client

