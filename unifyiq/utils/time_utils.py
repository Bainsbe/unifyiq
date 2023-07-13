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


def get_prev_cron_ts(cron_expr):
    """
    Returns the timestamp in seconds for the previous execution based on cron_expression.
    """
    base_time = datetime.datetime.now()
    cron = croniter(cron_expr, base_time)
    previous_execution = cron.get_prev(datetime.datetime)
    return int(previous_execution.timestamp())


def get_slack_ts(ts):
    return "{:.6f}".format(ts)
