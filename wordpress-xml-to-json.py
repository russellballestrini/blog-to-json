from datetime import datetime

from time import mktime

from sys import argv

from json import dumps

import xmltodict

if len(argv) != 2:
    print("usage: python {} wp-exported-posts.xml".format(argv[0]))
    exit(1)

with open(argv[1], 'r') as wp_exported_posts_file:
    document = xmltodict.parse(wp_exported_posts_file.read())

def get_timestamp(date_str):
    return int(mktime(datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').timetuple()))

def get_comment_dict(comment):
    return {
        'date'       : comment['wp:comment_date'],
        'timestamp'  : get_timestamp(comment['wp:comment_date']),
        'author'     : comment['wp:comment_author'],
        'email'      : comment['wp:comment_author_email'],
        'content'    : comment['wp:comment_content'],
    }

def get_comments_from_post(post):
    if 'wp:comment' not in post:
        return []
    comments = []
    for comment in post['wp:comment']:
        if isinstance(comment, dict):
            comments.append(get_comment_dict(comment))
    return comments

posts = {}

for post in document['rss']['channel']['item']:
    name = post['wp:post_name']
    posts[name] = {
      'name'     : name,
      'link'     : post['link'],
      'title'    : post['title'],
      'date'     : post['wp:post_date'],
      'timestamp': get_timestamp(post['wp:post_date']),
      'content'  : post['content:encoded'],
      'comments' : get_comments_from_post(post),
    }

print(dumps(posts, indent=2))