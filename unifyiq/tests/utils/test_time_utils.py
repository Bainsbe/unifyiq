import datetime
import unittest

from utils import time_utils


class TimeUtilTest(unittest.TestCase):
    def test_get_slack_ts(self):
        res = time_utils.get_slack_ts(1620835200)
        exp = "1620835200.000000"
        self.assertEqual(res, exp)

    def test_get_cron_interval(self):
        res = time_utils.get_cron_interval("*/5 * * * *")
        exp = 300
        self.assertEqual(res, exp)
        res = time_utils.get_cron_interval("0 0 * * *")
        exp = 86400
        self.assertEqual(res, exp)

    def test_get_prev_cron_ts(self):
        res = time_utils.get_prev_cron_ts("*/5 * * * *", base_time=datetime.datetime(2023, 1, 1, 0, 0, 0))
        exp = datetime.datetime(2022, 12, 31, 23, 55, 0).timestamp()
        self.assertEqual(res, exp)
        res = time_utils.get_prev_cron_ts("0 0 * * *", base_time=datetime.datetime(2023, 1, 1, 0, 0, 0))
        exp = datetime.datetime(2022, 12, 31, 0, 0, 0).timestamp()
        self.assertEqual(res, exp)

    def test_format_utc_timestamp(self):
        res = time_utils.format_utc_timestamp(1620835200)
        exp = "2021-05-12 16:00:00"
        self.assertEqual(res, exp)


if __name__ == '__main__':
    unittest.main()
