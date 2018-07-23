from datetime import datetime

from time import mktime


def get_timestamp(date_str):
    return int(mktime(datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').timetuple()))
