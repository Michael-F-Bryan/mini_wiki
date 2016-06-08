import yaml



class PageError(Exception):
    """
    A generic exception for all issues with pages.
    """


class Page:
    def __init__(self, filename=None, content=None, title=None, repo=None):
        self.filename = filename
        self.content = content
        self.repo = repo

        self.config = {}
        self.config['title'] = title

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

    def __str__(self):
        return self.format()



