import datetime


def current_time():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')