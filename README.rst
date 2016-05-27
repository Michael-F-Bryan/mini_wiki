====
wiki
====

.. image:: https://readthedocs.org/projects/mini-wiki/badge/?version=latest
:target: http://mini-wiki.readthedocs.io/en/latest/?badge=latest

A super lightweight wiki framework.


Description
===========

A framework to help quickly and easily design a wiki that stores pages as text
files on disk instead of using a database as a backend. It uses git behind the
scenes, so every edit, creation or deletion is recorded using version control.


Installation
============

To install, first grab the source code::

    git clone https://github.com/Michael-F-Bryan/mini_wiki

Then navigate to the project's folder and install::

    python3 setup.py install


Usage
=====

To create a new wiki, run ::

    python3 -m mini_wiki /path/to/wiki

Then start the dev server so you can see if it worked::

    cd /path/to/wiki
    python3 manage.py runserver

