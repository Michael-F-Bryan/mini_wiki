#!/usr/bin/env python3
"""
A script that will create an empty wiki.
"""

import os
import argparse
import shutil

project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def path_check(parser, arg):
    path = os.path.abspath(arg)

    if os.path.exists(path):
        parser.error('{} already exists'.format(path))
    else:
        return path

def create_wiki(path):
    sample = os.path.join(project_dir, '_sample')
    shutil.copytree(sample, path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dest', type=lambda arg: path_check(parser, arg),
            help='The location to create your wiki')

    args = parser.parse_args()
    create_wiki(args.dest)


if __name__ == "__main__":
    main()
