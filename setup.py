#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Setup file for wiki.

    This file was generated with PyScaffold 2.5.6, a tool that easily
    puts up a scaffold for your new Python project. Learn more under:
    http://pyscaffold.readthedocs.org/
"""

import sys
from setuptools import setup, find_packages
import versioneer
import configparser

config = configparser.ConfigParser()
config.read('./setup.cfg')
config = config['metadata']

setup(
        name=config['name'],
        version=versioneer.get_version(),
        description=config['summary'],
        long_description=open('README.rst').read(),
        author=config['author'],
        author_email=config['author-email'],
        url=config['home-page'],
        license=config['license'],

        packages=['mini_wiki'],

        install_requires=[
            'flask',
            'flask-login',
            'flask-sqlalchemy',
            'flask-script',
            'flask-migrate',
            'pyYAML',
            'gitpython',
            'markdown',

            'pytest',
            'coverage',
            'pytest-flask',
            ],

        cmdclass=versioneer.get_cmdclass(),
        include_package_data=True,
)
