==============
Implementation
==============

Here you'll find almost all the information you need to understand how this
wiki framework works.

General Procedure
=================

This is a brief overview of what happens every time a page is requests (all
file locations are relative to the wiki's root directory). In general, all
pages and articles are stored in the "/pages" directory.

Retrieving Files
----------------

1. User requests "/pages/blah"
#. Flask checks to see if "/pages/blah.md" or "/pages/blah/index.md" exist
#. If it does, then read the front matter for the file
#. If the user isn't allowed to view that page, give them an error message
#. Else, read the contents of the file, convert it from markdown to html, then
   substitute that html into the "content" section of a predefined template
#. Return result to user

Making a Change
---------------

1. User tries to edit the page by going to "/edit?path=/pages/blah.md" (the "/"
   character is html encoded and would look like "%52" or whatever)
#. Flask checks if the file exists and read/write permissions, if not then 
   create a new one at that location
#. Give the user a page with an embedded markdown editor and (if applicable)
   pre-populated with whatever text was in the file.
#. Once the user has finished his/her work, write the contents to the file and
   then try to commit just that file to git.
#. If the commit is unsuccessful (merge conflict), then send the user back to
   the editor, this time with the contents of the same file. Git will have put
   ">>>", "===", and "<<<" where the merge conflict is.
#. Repeat last step as required
#. Redirect user back to the page once they're finished editing and the commit
   was successful.

Or more generally:

1. Check permissions
#. Make the change
#. Attempt commit
#. Resolve any merge conflicts if necessary


Front Matter
============

Similar to Jekyll_, each page has a section at the beginning called the "front
matter". This section is nothing more than some YAML describing metadata about
the page, enclosed between a pair of "---" lines.

Generally, the front matter can contain just about any valid YAML, however
there are a couple required fields, as well as several optional ones. All
fields are case insensitive.

Required:

Title 
    The title of the page
Last_edited 
    A tuple of the username of the last person to edit the page, and a 
    timestamp 

Optional:

Tags
    Some tags to associate the page with
Permissions 
    A dictionary of group names and their permissions ("read/write", "read", 
    "none") 
Filetype
    If multiple render engines are supported, specify the filetype so that the
    correct engine can be used
Layout
    The html template to use when displaying this page. Defaults to
    "default.html"

Here is an example front matter::

    ---
    title: My awesome page
    last_edited: 
        - michael
        - 2016/05/23 19:11:00
    permissions:
        admin: read/write
        team: read
        default: none
    ---


.. _Jekyll: https://jekyllrb.com/
