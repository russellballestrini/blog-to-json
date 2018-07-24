import miniuri

from .utils import get_disqus_timestamp as get_timestamp


def get_comment_dict(comment, thread_id):
    # Disqus comments have no parent ID if they're at the root
    parent_id = comment.get('parent')
    if parent_id is None:
        parent_id = int(0)
    else:
        parent_id = int(parent_id['@dsq:id'])

    return {
        'id'         : int(comment['@dsq:id']),
        'parent_id'  : parent_id,
        'author_ip'  : comment['ipAddress'],
        'author'     : comment['author']['name'],
        'email'      : comment['author']['email'],
        'content'    : comment['message'],
        'date'       : comment['createdAt'],
        'timestamp'  : get_timestamp(comment['createdAt']),
    }


def get_comments_from_post(thread_id, posts):
    comments = []
    for post in posts:
      if post['thread']['@dsq:id'] == thread_id:
        if post['isDeleted'] != 'true':
          comments.append(get_comment_dict(post, thread_id))
    return comments


def disqus_xml_dict_to_normalized_dict(document):
    posts = {}
    for post in document['disqus']['thread']:
        parsed_uri = miniuri.Uri(post['link'])
        name = parsed_uri.relative_uri
        posts[name] = {
          'name'     : name,
          'id'       : post['@dsq:id'],
          'link'     : post['link'],
          'title'    : post['title'],
          'date'     : post['createdAt'],
          'timestamp': get_timestamp(post['createdAt']),
          'comments' : get_comments_from_post(post['@dsq:id'], document['disqus']['post']),
          'metadata' : {},
        }
    return posts
