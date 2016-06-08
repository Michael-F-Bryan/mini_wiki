import os
import pytest
from flask import url_for


class TestViews:
    def test_homepage(self, client):
        client.get(url_for('main.homepage'))

    def test_404(self, client):
        client.get('iuewsdfhuiwcfhbewdcewf')

    # def test_500(self, client):
    #     client.get(url_for('server_error'))
