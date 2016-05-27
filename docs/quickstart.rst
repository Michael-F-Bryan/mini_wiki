.. _quickstart:

==========
Quickstart
==========

This short guide is probably the first thing you should do once you finish
installing the mini_wiki package. It'll teach you:

* How to create a new wiki
* Starting up the dev server and checking out your new wiki
* Editing some metadata about your website
* Creating your first page

.. note::
    A lightweight server that's probably good enough if you're just using 
    this as a personal wiki and starting it up when you need it. Once you 
    start getting multiple users or need to have the wiki online 24/7, you 
    probably want to check out the deployment guide (not yet finished).


Creating a Wiki
===============

Creating a new wiki is actually fairly easy to do. The package comes with a
``__main__.py`` helper script, so all you need to do is run the following::

    python3 -m mini_wiki /path/to/new/wiki


Starting The Wiki Server
========================

.. note::
    The ``manage.py`` file is the main utility script that allows you to
    administer your wiki. So it might be a good idea to check out it's help
    text by running ``manage.py --help``.

The dev server will be able to sit in a terminal and let you navigate your
wiki, changing pages and doing other interesting things. Under the hood, it's
just the standard Flask dev server.

Before starting up the server, it's always a good idea to initialise your user
database. This is just a really small sqlite database that will contain details
of the people who are registered with your wiki and allowed to log in. Do this
with::

    python3 manage.py db init

To get the server going, run the following from your wiki's root directory::

    python3 manage.py runserver

You can also specify the port and host for the server to run on by using
command line arguments. By default the server runs on
`<http://127.0.0.1:5000/>`_, so the only computer able to access it is yours. 
Say you wanted to run the server on port 8080 and allow anyone to view it by
navigating to your IP address, you would do something like this::

    python3 manage.py runserver --host 0.0.0.0 --port 8080
