import datetime

def date_from_string(date_string):
    DATE_FORMAT = '%Y-%m-%d'
    return datetime.datetime.strptime(date_string, DATE_FORMAT)

def string_from_date(date):
    DATE_FORMAT = '%Y-%m-%d'
    return date.strftime(DATE_FORMAT)
