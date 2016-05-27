from yaml import load
from collections import namedtuple

Page = namedtuple('Page', ('filename', 'front_matter', 'contents'))

class ParseError(Exception):
    pass


def read_front_matter(filename):
    front_matter = []
    
    with open(filename) as f:
        if '---' not in f.readline():
            raise ParseError('No Front Matter marker found')

        for line in f:
            if line.strip() == '---':
                break
            elif not line:
                raise ParseError('Front Matter cannot contain blank lines')
            else:
                front_matter.append(line.strip())

        content = ''.join(f.readlines())

    front_matter = '\n'.join(front_matter)
    
    return Page(
            filename=filename,
            front_matter=load(front_matter), 
            contents=content)



