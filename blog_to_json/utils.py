from datetime import datetime

from time import mktime


def make_timestamp_from_datetime(datetime_object):
    return int(mktime(datetime_object.timetuple()))

def get_wordpress_timestamp(date_str):
    datetime_object = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return make_timestamp_from_datetime(datetime_object)

def get_disqus_timestamp(date_str):
    datetime_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    return make_timestamp_from_datetime(datetime_object)
