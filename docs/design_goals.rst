============
Design Goals
============

Must-Have Features
==================

* Backed by git (every change recorded using version control)
* Stored as plain text files on the filesystem
* All pages/articles editable through either a text editor or the wiki's
  embedded editor
* Pages stored as markdown or in a similar markup language (a la Jekyll)
* Customizable HTML templates for the wiki's various pages
* Simple and easy to use
* Multi-user
* All metadata kept inside the file's "Front Matter" (similar to Jekyll)


Would Be Cool To Have
=====================

* Can export entire wiki to static HTML pages so you can serve a read-only
  version using something like Nginx (again, similar to Jekyll)
* Editor built into the wiki website with previewing of the processed markdown 
  content
* Each edit, new page, deletion or other change is recorded using a git commit.
  All commits have useful messages (like "[user] created a page:
  /path/to/page")
* Backups are dead simple and easy to understand/implement/schedule
* Access restrictions for pages (perhaps embedded in the front matter)
* Upload files and images, allowing users to link to them
* Support merging of pages if two people are editing the same thing at the same
  time (similar to git merges)
* Deal with merge conflicts appropriately, possibly the same way you do in
  git
* Simple interface to cron-like backups and jobs (probably just use cron under
  the hood)
* Users get their own homepage
* Built in templates to make page creation easier
* Permission groups (e.g. admin, team, no-permissions)


Will Not Be/Do
==============

* No collaborative editing (like google docs)
* No embedded chats
* No huge backend database. User details might be saved in a sqlite database
  for ease and performance, but there'll be a simple csv file containing the
  usernames, emails and password hashes.

