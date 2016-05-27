from yaml import load
from collections import namedtuple
from ..errors import ParseError


Page = namedtuple('Page', ('filename', 'front_matter', 'contents'))

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
    front_matter = load(front_matter)

    if 'filetype' not in front_matter:
        front_matter['filetype'] = 'markdown'

    content = parse_content(content, front_matter['filetype'])
    
    return Page(
            filename=filename,
            front_matter=front_matter, 
            contents=content)

def parse_content(content, filetype):
    if filetype.lower() in ('markdown', 'md'):
        from markdown import markdown
        return markdown(content, output_format='html5')
    else:
        raise ParseError('No available rendering engine')


