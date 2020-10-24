import datetime
from dateutil.parser import parse


def datetime_from_str(date_str):
    return parse(date_str)


def datetime_from_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def format_currency(amount):
    return "${:,.2f}".format(amount)