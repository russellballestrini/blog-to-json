wordpress-xml-to-json
######################

This tool will convert Wordpress XML dumps to JSON.

It is opinionated and removes lots of data.

install::

 git clone https://github.com/russellballestrini/wordpress-xml-to-json.git
 cd wordpress-xml-to-json
 pip install -r requirements.txt

how to use::

 python wordpress-xml-to-json.py example.xml 

example of schema:

.. code-block:: json

  "homegrown-python-bread-crumb-module": {
    "name": "a-homegrown-python-bread-crumb-module", 
    "title": "A homegrown python bread crumb module", 
    "timestamp": 1293995686, 
    "comments": [
      {
        "date": "2011-04-03 10:33:07", 
        "timestamp": 1301841187, 
        "content": "Hi, this was just what I needed, did a few modifications but basically worked out of the box. Thanks for posting", 
        "email": "oops", 
        "author": "Kristian"
      }, 
      {
        "date": "2011-04-03 14:19:46", 
        "timestamp": 1301854786, 
        "content": "I'm interested in the modifications, I just placed the code into bitbucket.  Feel free to branch it.  \n\nI'm also interested in seeing your project that you used it in.  Thanks", 
        "email": "oops", 
        "author": "Russell Ballestrini"
      }
    ], 
    "content": "<p><strong>I wrote <a href=\"https://bitbucket.org/russellballestrini/bread/raw/tip/bread.py\">bread.py</a> a few days ago.</strong> <a href=\"https://bitbucket.org/russellballestrini/bread/raw/tip/bread.py\">Bread.py</a> is a simple to use python breadcrumb module. \n</p>\n\n<p>\nThe bread object accepts a url string and grants access to the url crumbs (parts) or url links (list of hrefs to each crumb) .\n</p>\n\n<p>\nI have released <a href=\"https://bitbucket.org/russellballestrini/bread/raw/tip/bread.py\">bread.py</a> into the public domain and you may view the full source code here: <a href=\"https://bitbucket.org/russellballestrini/bread/src\">https://bitbucket.org/russellballestrini/bread/src</a>\n</p>\n\n<p>\n<strong>Update</strong>\n</p>\n\n<p>\nI recently revisited this module and wrote a tutorial on how to <a href=\"http://russell.ballestrini.net/add-a-breadcrumb-subscriber-to-a-pyramid-project-using-4-simple-steps/\">Add a Breadcrumb Subscriber to a Pyramid project using 4 simple steps</a>.\n</p>\n\n<ul>\n<li>Demo of bread.py: <a href=\"http://school.yohdah.com/\">http://school.yohdah.com/</a></li>\n<li>Pyrawiki will use bread.py</li> \n</ul>\n\n<br />\n\n<strong>You should follow me on twitter <a href=\"http://twitter.com/russellbal\" target=\"_blank\">here</a></strong>\n\n<span style=\"font-size: 10px;\">\n<script src=\"https://bitbucket.org/russellballestrini/bread/src/50a1a20fc3f3/bread.py?embed=t\"></script>\n</span>", 
    "link": "http://russell.ballestrini.net/a-homegrown-python-bread-crumb-module/", 
    "date": "2011-01-02 14:14:46"
  } 

misc
====

* A related process / tool to convert wordpress into rst or md files (ReStructuredText or MarkDown) is `pelican-import <http://docs.getpelican.com/en/latest/importer.html>`_.  I suggest checking it out, even if you do not plan to use Pelican as your static site generator.

* After using `pelican-import <http://docs.getpelican.com/en/latest/importer.html>`_ I had about 150 `.rst` files and I decided to put the date in the filename, so I wrote this short bash script tool to do the renames

 .. code-block:: bash

  files=`ls *.rst`

  for file in $files:
    do
      the_date=`grep ':date:' "$file" | awk '{ print $2; }'`
      mv "$file" "$the_date-$file"
    done

* category and tags have different meanings and assumptions between wordpress and pelican.  As a result I decided to change all my categories to tags using this command:

 .. code-block:: bash

  sed -i'' -e 's/:category:/:tags:/g' *.rst
