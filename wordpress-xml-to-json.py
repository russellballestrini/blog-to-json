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
        'id'         : int(comment['wp:comment_id']),
        'parent_id'  : int(comment['wp:comment_parent']),
        'author_ip'  : comment['wp:comment_author_IP'],
        'author'     : comment['wp:comment_author'],
        'email'      : comment['wp:comment_author_email'],
        'content'    : comment['wp:comment_content'],
        'date'       : comment['wp:comment_date'],
        'timestamp'  : get_timestamp(comment['wp:comment_date']),
    }

def get_comments_from_post(post):
    comments = []
    if 'wp:comment' not in post:
        return comments
    for comment in post['wp:comment']:
        if isinstance(comment, dict):
            comments.append(get_comment_dict(comment))
    return comments

def get_metadata_from_post(post):
    metadata = {}
    if 'wp:postmeta' not in post:
      return metadata
    for meta in post['wp:postmeta']:
      if isinstance(meta, dict):
        metadata[meta['wp:meta_key']] = meta['wp:meta_value']
    return metadata

posts = {}

for post in document['rss']['channel']['item']:
    name = post['wp:post_name']
    posts[name] = {
      'name'     : name,
      'id'       : post['wp:post_id'],
      'link'     : post['link'],
      'title'    : post['title'],
      'content'  : post['content:encoded'],
      'date'     : post['wp:post_date'],
      'timestamp': get_timestamp(post['wp:post_date']),
      'comments' : get_comments_from_post(post),
      'metadata' : get_metadata_from_post(post),
    }

print(dumps(posts, indent=2))
