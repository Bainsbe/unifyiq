import datetime

from croniter import croniter


def get_cron_interval(cron_expr):
    """
    Returns the interval between two consecutive runs of the cron job in seconds.
    """
    base_time = datetime.datetime.now()

    cron = croniter(cron_expr, base_time)
    next_execution = cron.get_next(datetime.datetime)
    previous_execution = cron.get_prev(datetime.datetime)

    window_size = next_execution - previous_execution
    return window_size.total_seconds()


def get_ts_for_beginning_of_curr_day():
    """
    Returns the timestamp in seconds for the beginning of the current day.
    """
    now = datetime.datetime.now()
    return int(datetime.datetime(now.year, now.month, now.day).timestamp())
