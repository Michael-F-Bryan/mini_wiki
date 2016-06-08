import os
import yaml
import markdown



class PageError(Exception):
    """
    A generic exception for all issues with pages.
    """

class ParseError(PageError):
    """
    Exception raised when there was an error parsing a page.
    """

class NoRenderEngineError(PageError):
    """
    Exception raised when there are no supported render engines.
    """


class Page:
    def __init__(self, filename=None, content=None, title=None, repo=None, 
            config=None):
        self.filename = filename
        self.content = content or ''
        self.repo = repo

        self.config = config if config else {}

        if config is not None and title is not None:
            raise ValueError("Can't pass in both the title and a config dict")

        if config is None and title is None:
            raise ValueError('Must pass in either a title or a config dictionary')

        if 'title' not in self.config and title:
            self.config['title'] = title

        try:
            self.title = self.config['title']
        except KeyError as e:
            raise PageError('Every page must have a title') from e

    def save(self):
        """
        Write a copy of the 
        """
        if not self.filename:
            raise PageError('No filename set')
        elif not self.repo:
            raise PageError('No git repository set')
        else:
            with open(self.filename, 'w') as f:
                f.write(self.format())

            # Then do a `git add some_file.txt`
            self.repo.index.add([self.filename])

    def commit(self, message, author):
        """
        Commit the file. (i.e. run "git commit -m $message")

        Parameters
        ----------
        message: str
            The commit message
        author: git.Actor
            The person making a change to the file
        """
        self.save()  # git add this_file.txt
        self.repo.index.commit(message, author=author)

    def header(self):
        """
        Create a jekyll-style header for the file.
        """
        head = []
        head.append('---')
        config = yaml.dump(self.config, default_flow_style=False).strip()
        head.append(config)
        head.append('---')

        return '\n'.join(head)

    def format(self):
        """
        Get a formatted form of the header and page content.
        """
        text = []
        text.append(self.header())
        text.append('')
        text.append(self.content)
        return '\n'.join(text)

    def to_html(self):
        """
        Get a html version of the page's content. 

        Depending on the 'format' key in the page's metadata, different 
        rendering methods will be used.

        Rendering Methods:
        markdown
            Use the [markdown](https://pythonhosted.org/Markdown/) library.
        html
            Don't do anything to the content and return it as-is.
        """
        if self.config.get('format', 'markdown').lower() in ('markdown', 'md'):
            return markdown.markdown(self.content)
        elif self.config.get('format', '').lower() in ('html'):
            return self.content
        else:
            raise NoRenderEngineError('No render engine for file: {}'.format(self.filename))


    def __str__(self):
        return self.format()

    @classmethod
    def from_file(cls, filename):
        """
        Given a path to a file, parse its contents and get the corresponding 
        Page object.  
        """
        if not os.path.exists(filename):
            raise FileNotFoundError("{} doesn't exist".format(filename))

        text = open(filename).read()
        header, body = cls.parse_text(text)

        new_page = cls(filename=filename, config=header, content=body)
        return new_page

    @staticmethod
    def parse_text(text):
        """
        Given a string of text, parse it and retrieve the header and content.

        The text must have the following format:
        - Line with '---' to specify the start of the header section
        - One or more lines of valid YAML that contain metadata about the file
        - Line with '---' to specify the end of the header section
        - A blank line
        - Body of the document (may be empty)

        Parameters
        ----------
        text: str
            The text to parse

        Returns
        -------
        header: dict
            A dictionary containing metadata about the file
        body: str
            The body of the file

        Raises
        ------
        ParseError
            When the file isn't formatted correctly

        """
        lines = (line for line in text.splitlines())

        # Read in the first line
        current_line = next(lines)
        if current_line.strip() != '---':
            raise ParseError('File must have a header section')

        # Read from line 2 up to and including the end of the header
        current_line = next(lines)
        header_buffer = []
        while current_line.strip() != '---':
            if current_line.strip() == '':
                # Found a blank line
                raise ParseError('Empty line in page header')
            else:
                header_buffer.append(current_line)

            current_line = next(lines)

        # Parse the header
        header = yaml.load('\n'.join(header_buffer))

        # Next read the empty line after the header
        current_line = next(lines)
        if current_line.strip() != '':
            raise ParseError('There must be an empty line after the header section')
        
        # Every line from now on is the body, so just concatenate that
        body = '\n'.join(lines)
        body = body.strip()

        return header, body
