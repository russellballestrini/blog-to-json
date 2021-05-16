blog-to-json
######################

This tool will convert various blog dumps to a standard JSON format.

For example:

* Wordpress XML dumps to JSON
* Disqus XML dumps to JSON
* Graphcomment WordPress XML dumps to JSON

It is opinionated and may at times remove data.

install
===========

::

 git clone https://github.com/russellballestrini/blog-to-json.git
 cd blog-to-json
 python setup.py develop

Wordpress XML to JSON
========================

how to use::

 wordpress-xml-to-json example.xml 

example of schema:

.. code-block:: json

 {
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
         "author": "Kristian",
         "author_ip": "192.168.1.5"
       }, 
       {
         "date": "2011-04-03 14:19:46", 
         "timestamp": 1301854786, 
         "content": "I'm interested in the modifications, I just placed the code into bitbucket.  Feel free to branch it.  \n\nI'm also interested in seeing your project that you used it in.  Thanks", 
         "email": "oops", 
         "author": "Russell Ballestrini",
         "author_ip": "192.168.1.6"
       }
     ], 
     "content": "<p><strong>I wrote <a href=\"https://bitbucket.org/russellballestrini/bread/raw/tip/bread.py\">bread.py</a> a few days ago.</strong> <a href=\"https://bitbucket.org/russellballestrini/bread/raw/tip/bread.py\">Bread.py</a> is a simple to use python breadcrumb module. \n</p>\n\n<p>\nThe bread object accepts a url string and grants access to the url crumbs (parts) or url links (list of hrefs to each crumb) .\n</p>\n\n<p>\nI have released <a href=\"https://bitbucket.org/russellballestrini/bread/raw/tip/bread.py\">bread.py</a> into the public domain and you may view the full source code here: <a href=\"https://bitbucket.org/russellballestrini/bread/src\">https://bitbucket.org/russellballestrini/bread/src</a>\n</p>\n\n<p>\n<strong>Update</strong>\n</p>\n\n<p>\nI recently revisited this module and wrote a tutorial on how to <a href=\"http://russell.ballestrini.net/add-a-breadcrumb-subscriber-to-a-pyramid-project-using-4-simple-steps/\">Add a Breadcrumb Subscriber to a Pyramid project using 4 simple steps</a>.\n</p>\n\n<ul>\n<li>Demo of bread.py: <a href=\"http://school.yohdah.com/\">http://school.yohdah.com/</a></li>\n<li>Pyrawiki will use bread.py</li> \n</ul>\n\n<br />\n\n<strong>You should follow me on twitter <a href=\"http://twitter.com/russellbal\" target=\"_blank\">here</a></strong>\n\n<span style=\"font-size: 10px;\">\n<script src=\"https://bitbucket.org/russellballestrini/bread/src/50a1a20fc3f3/bread.py?embed=t\"></script>\n</span>", 
     "link": "http://russell.ballestrini.net/a-homegrown-python-bread-crumb-module/", 
     "date": "2011-01-02 14:14:46"
   }
 }

Graphcomment WordPress XML to JSON
==================================
Note that this uses Python 2.7

how to use::

 graphcomment-xml-to-json grcomm.wxr --host "https://abc.xyz"

example of schema:

.. code-block:: json

  "posts_jupyter-orgmode": {
    "content": null,
    "link": "https://abc.xyz/posts/jupyter-orgmode/",
    "name": "posts_jupyter-orgmode",
    "title": "Reflections",
    "date": "2020-09-22 15:57:34",
    "timestamp": 1600790254,
    "id": "5f6a1eee2f57815d17188de2",
    "comments": [
      {
        "content": "Thanks!!!!! a lot!!!",
        "parent_id": null,
        "author": "SamTux",
        "date": "2021-04-13 03:16:54",
        "timestamp": 1618283814,
        "id": "60750d2613ebd3704ec85f6f",
        "author_ip": "190.25.34.217",
        "email": "redacted"
      }
    ],
    "metadata": {}
  },


Why?
============

It's your data, thats why!

I created and used this tool during my `Migration from WordPress to Pelican <http://russell.ballestrini.net/migrating-from-wordpress-to-pelican/>`_. Others have used this tool to migrate comments from Disqus to `Remarkbox <https://www.remarkbox.com>`_.

