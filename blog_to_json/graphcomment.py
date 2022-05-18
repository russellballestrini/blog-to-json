from .utils import get_wordpress_timestamp as get_timestamp


try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse

def get_comment_dict(comment):
    return {
        'id'         : comment['wp:comment_id'],
        'parent_id'  : comment['wp:comment_parent'],
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
        # some posts do not have comments.
        return comments

    post_comments = post['wp:comment']
    if not isinstance(post_comments, list):
        # some posts have 1 comment, which is type Dict, so wrap in list.
        post_comments = [post_comments]

    for comment in post_comments:
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

def comment_cleaner(postlist, sitename):
    clean_list = []
    for post in postlist:
        if sitename in post['link']:
            clean_list.append(post)
    return clean_list

def extract_name(url_copy):
    upath = urlparse(url_copy).path
    if upath[0] == '/' and upath[-1] == '/':
        upath=upath[1:-1].replace('/','_')
    return upath


def graphcomment_xml_dict_to_normalized_dict(document, *args):
    posts = {}
    postlist = comment_cleaner(document['rss']['channel']['item'], args[0])
    for post in postlist:
        name = extract_name(post['link'])
        post_type = post['wp:post_type']
        if post_type != "post":
            # an attachment might have the same "post_name" as an actual post.
            continue
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
    return posts
