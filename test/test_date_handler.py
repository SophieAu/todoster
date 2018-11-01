import unittest
from unittest.mock import patch
import datetime
from freezegun import freeze_time
from isoweek import Week

from todoster import date_handler

class TestDatetimeHandler(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_valid_date_format(self):
        dot_with_zeros = "01.01."
        dot_standard = "1.1."
        dot_without_trailing_dot = "1.1"
        dot_with_short_year = "1.1.18"
        dot_with_long_year = "1.1.2018"
        dash_with_zeros = "01/01"
        dash_standard = "1/1"
        dash_with_short_year = "1/1/18"
        dash_with_long_year = "1/1/2018"
        iso = "2018-01-01"

        self.assertTrue(date_handler.is_valid_date_format(dot_with_zeros))
        self.assertTrue(date_handler.is_valid_date_format(dot_standard))
        self.assertTrue(date_handler.is_valid_date_format(dot_without_trailing_dot))
        self.assertTrue(date_handler.is_valid_date_format(dot_with_short_year))
        self.assertTrue(date_handler.is_valid_date_format(dot_with_long_year))
        self.assertTrue(date_handler.is_valid_date_format(dash_with_zeros))
        self.assertTrue(date_handler.is_valid_date_format(dash_standard))
        self.assertTrue(date_handler.is_valid_date_format(dash_with_short_year))
        self.assertTrue(date_handler.is_valid_date_format(dash_with_long_year))
        self.assertTrue(date_handler.is_valid_date_format(iso))

        invalid_iso_date = "2018-24-37" # should be true because I'm only checking for the format
        self.assertTrue(date_handler.is_valid_date_format(invalid_iso_date))

        missing_day_in_date = "01.2018"
        invalid_date_format = "hjkdgkasd"

        self.assertFalse(date_handler.is_valid_date_format(missing_day_in_date))
        self.assertFalse(date_handler.is_valid_date_format(invalid_date_format))

    @freeze_time("2018-01-01")
    def test_is_past_date(self):
        empty_date = ''
        past_date = '2017-09-12'
        current_date = '2018-01-01'
        future_date = '2018-02-02'

        self.assertFalse(date_handler.is_past_date(empty_date))
        self.assertTrue(date_handler.is_past_date(past_date))
        self.assertFalse(date_handler.is_past_date(current_date))
        self.assertFalse(date_handler.is_past_date(future_date))

    @freeze_time("2018-01-05")
    def test_format_date(self):
        dot_with_zeros = "05.01."
        dot_without_zeros = "5.1."
        dash_with_zeros = "05/01"
        dash_without_zeros = "5/1"
        iso = "2018-01-05"
        self.assertEqual(date_handler.format_date(dot_with_zeros), datetime.date(2018, 1, 5))
        self.assertEqual(date_handler.format_date(dot_without_zeros), datetime.date(2018, 1, 5))
        self.assertEqual(date_handler.format_date(dash_with_zeros), datetime.date(2018, 1, 5))
        self.assertEqual(date_handler.format_date(dash_without_zeros), datetime.date(2018, 1, 5))
        self.assertEqual(date_handler.format_date(iso), datetime.date(2018, 1, 5))

        dot_with_short_year = "1.5.18"
        dot_with_long_year = "1.5.2018"
        self.assertEqual(date_handler.format_date(dot_with_short_year), datetime.date(2018, 5, 1))
        self.assertEqual(date_handler.format_date(dot_with_long_year), datetime.date(2018, 5, 1))

        future_dot = "01.01."
        past_dot = "01.01.2018"
        self.assertEqual(date_handler.format_date(future_dot), datetime.date(2019, 1, 1))
        self.assertEqual(date_handler.format_date(past_dot), datetime.date(2018, 1, 1))

        # pass

    @patch('isoweek.Week.thisweek')
    def test_is_past_week(self, isoweek_mock):
        isoweek_mock.return_value = Week.fromstring("2018W18")
        empty_week = ''
        past_week = '2018W02'
        current_week = '2018W18'
        future_week = '2018W50'

        self.assertFalse(date_handler.is_past_week(empty_week))
        self.assertTrue(date_handler.is_past_week(past_week))
        self.assertFalse(date_handler.is_past_week(current_week))
        self.assertFalse(date_handler.is_past_week(future_week))

    def test_is_valid_week(self):
        small_w = "w1"
        small_w_with_zeros = "w01"
        large_w = "W1"
        week_dash_short = "w01/12"
        week_dash_long = "w12/2018"
        week_minus_short = "w12-12"
        year_then_week = "2018-w12"
        iso = "2018W12"

        week_too_long = "W012"
        random_string = "sddags"
        no_week_signifier = "01-2018"

        self.assertTrue(date_handler.is_valid_week_format(small_w))
        self.assertTrue(date_handler.is_valid_week_format(small_w_with_zeros))
        self.assertTrue(date_handler.is_valid_week_format(large_w))
        self.assertTrue(date_handler.is_valid_week_format(week_dash_short))
        self.assertTrue(date_handler.is_valid_week_format(week_dash_long))
        self.assertTrue(date_handler.is_valid_week_format(week_minus_short))
        self.assertTrue(date_handler.is_valid_week_format(year_then_week))
        self.assertTrue(date_handler.is_valid_week_format(iso))
        self.assertFalse(date_handler.is_valid_week_format(week_too_long))
        self.assertFalse(date_handler.is_valid_week_format(random_string))
        self.assertFalse(date_handler.is_valid_week_format(no_week_signifier))

    @patch('isoweek.Week.thisweek')
    def test_format_week(self, isoweek_mock):
        isoweek_mock.return_value = Week.fromstring("2018W18")

        lower_w = "w23"
        upper_w = "W23"
        week_dash_year = "w23/2018"
        year_dash_week = "2018/w23"
        week_minus_year = "w23-2018"
        year_week = "2018w23"
        lower_w_next_year = "w10"

        self.assertEqual(date_handler.format_week(lower_w), Week.fromstring("2018-W23"))
        self.assertEqual(date_handler.format_week(upper_w), Week.fromstring("2018-W23"))
        self.assertEqual(date_handler.format_week(week_dash_year), Week.fromstring("2018-W23"))
        self.assertEqual(date_handler.format_week(year_dash_week), Week.fromstring("2018-W23"))
        self.assertEqual(date_handler.format_week(year_week), Week.fromstring("2018-W23"))
        self.assertEqual(date_handler.format_week(week_minus_year), Week.fromstring("2018-W23"))
        self.assertEqual(date_handler.format_week(lower_w_next_year), Week.fromstring("2019-W10"))

    def test_get_week_from_date(self):
        date = datetime.date(2018, 10, 13)
        self.assertEqual(date_handler.get_week_from_date(date), Week.fromstring("2018W41"))


if __name__ == '__main__':
    unittest.main()
