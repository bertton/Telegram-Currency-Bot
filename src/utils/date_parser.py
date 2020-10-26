import datetime
from dateutil.parser import parse


def format_datetime(dateobj):
    date = None
    if isinstance(dateobj, int):
        date = datetime.datetime.fromtimestamp(dateobj)
    else:
        date = parse(dateobj)
    return date.strftime('%Y-%m-%d %H:%M')