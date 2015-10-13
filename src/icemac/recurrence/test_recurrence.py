import zope.publisher.browser
import pytz
import unittest
import datetime


class RecurrenceMixIn(object):
    """Mix-in to test ..recurrence.*."""

    def callFUT(self, adapter_name, datetime=None, start=None, end=None):
        from .recurrence import get_recurrences
        datetime = self.recurrence_start if datetime is None else datetime
        start = self.interval_start if start is None else start
        end = self.interval_end if end is None else end
        return list(get_recurrences(datetime, adapter_name, start, end))

    def info(self, adapter_name):
        from .recurrence import get_recurring
        from zope.globalrequest import setRequest
        from zope.i18n import translate
        request = self.get_request(HTTP_ACCEPT_LANGUAGE='en')
        setRequest(request)
        return translate(
            get_recurring(self.recurrence_start, adapter_name).info, request)


class TestMixIn(object):
    """Helper methods."""

    def get_datetime(self, args=(), tzinfo=None):
        """Create a datetime object.

        `args` ... time tuple
        If no `args` are given current time is returned.
        If `tzinfo` is None, UTC is used.

        """
        if tzinfo is None:
            tzinfo = pytz.utc
        if args:
            dt = datetime.datetime(*args)
        else:
            dt = datetime.datetime.now()
        return tzinfo.localize(dt)

    def get_request(self, **kw):
        """Get a request object on the right skin layer."""
        return zope.publisher.browser.TestRequest(**kw)


class InterfaceTests(unittest.TestCase):
    """Testing interfaces in ..recurrence.*"""

    now = datetime.date.today()

    def test_Daily_fulfills_IRecurringDateTime_interface(self):
        from zope.interface.verify import verifyObject
        from .interfaces import IRecurringDateTime
        from .recurrence import Daily
        self.assertTrue(verifyObject(IRecurringDateTime, Daily(self.now)))

    def test_Weekly_fulfills_IRecurringDateTime_interface(self):
        from zope.interface.verify import verifyObject
        from .interfaces import IRecurringDateTime
        from .recurrence import Weekly
        self.assertTrue(verifyObject(IRecurringDateTime, Weekly(self.now)))

    def test_BiWeekly_fulfills_IRecurringDateTime_interface(self):
        from zope.interface.verify import verifyObject
        from .interfaces import IRecurringDateTime
        from .recurrence import BiWeekly
        self.assertTrue(verifyObject(IRecurringDateTime, BiWeekly(self.now)))

    def test_MonthlyNthWeekday_fulfills_IRecurringDateTime_interface(self):
        from zope.interface.verify import verifyObject
        from .interfaces import IRecurringDateTime
        from .recurrence import MonthlyNthWeekday
        self.assertTrue(
            verifyObject(IRecurringDateTime, MonthlyNthWeekday(self.now)))

    def test_BiMonthlyNthWeekday_fulfills_IRecurringDateTime_interface(self):
        from zope.interface.verify import verifyObject
        from .interfaces import IRecurringDateTime
        from .recurrence import BiMonthlyNthWeekday
        self.assertTrue(
            verifyObject(IRecurringDateTime, BiMonthlyNthWeekday(self.now)))

    def test_MonthlyNthWeekdayFromEnd_fulfills_IRecurringDateTime_interface(
            self):
        from zope.interface.verify import verifyObject
        from .interfaces import IRecurringDateTime
        from .recurrence import MonthlyNthWeekdayFromEnd
        self.assertTrue(verifyObject(IRecurringDateTime,
                                     MonthlyNthWeekdayFromEnd(self.now)))

    def test_BiMonthlyNthWeekdayFromEnd_fulfills_IRecurringDateTime_interface(
            self):
        from zope.interface.verify import verifyObject
        from .interfaces import IRecurringDateTime
        from .recurrence import BiMonthlyNthWeekdayFromEnd
        self.assertTrue(verifyObject(IRecurringDateTime,
                                     BiMonthlyNthWeekdayFromEnd(self.now)))

    def test_Yearly_instance_fulfills_IRecurringDateTime_interface(self):
        from zope.interface.verify import verifyObject
        from .interfaces import IRecurringDateTime
        from .recurrence import Yearly
        self.assertTrue(verifyObject(IRecurringDateTime, Yearly(self.now)))


class WeeklyTests(RecurrenceMixIn, unittest.TestCase, TestMixIn):
    """Testing ..recurrence.Weekly"""

    def setUp(self):
        super(RecurrenceMixIn, self).setUp()
        self.recurrence_start = self.get_datetime((2013, 5, 3, 21, 45))
        self.interval_start = self.get_datetime((2014, 4, 1))
        self.interval_end = self.get_datetime((2014, 4, 30))

    def test_info_renders_weekday(self):
        self.assertEqual(u'Friday every week', self.info('weekly'))

    def test_returns_all_dates_in_interval_for_same_weekday(self):
        self.assertEqual(
            [self.get_datetime((2014, 4, 4, 21, 45)),
             self.get_datetime((2014, 4, 11, 21, 45)),
             self.get_datetime((2014, 4, 18, 21, 45)),
             self.get_datetime((2014, 4, 25, 21, 45))], self.callFUT('weekly'))
        self.assertEqual(self.recurrence_start.isoweekday(),
                         self.callFUT('weekly')[0].isoweekday())

    def test_does_not_start_before_datetime(self):
        self.assertEqual(
            [self.get_datetime((2014, 4, 18, 21, 45)),
             self.get_datetime((2014, 4, 25, 21, 45))],
            self.callFUT('weekly',
                         datetime=self.get_datetime((2014, 4, 18, 21, 45))))
        self.assertEqual(self.recurrence_start.isoweekday(),
                         self.callFUT('weekly')[0].isoweekday())

    def test_returns_empty_interval_if_datetime_after_interval_end(self):
        self.assertEqual(
            [], self.callFUT(
                'weekly', datetime=self.get_datetime((2014, 5, 1, 21, 45))))

    def test_interval_end_does_not_belong_to_interval(self):
        self.assertEqual(
            [], self.callFUT(
                'weekly', start=self.get_datetime((2014, 4, 24)),
                end=self.get_datetime((2014, 4, 25))))

    def test_interval_start_belongs_to_interval(self):
        self.assertEqual(
            [self.get_datetime((2014, 4, 4, 21, 45))],
            self.callFUT(
                'weekly', start=self.get_datetime((2014, 4, 4)),
                end=self.get_datetime((2014, 4, 5))))


class BiWeeklyTests(RecurrenceMixIn, TestMixIn, unittest.TestCase):
    """Testing ..recurrence.BiWeekly"""

    def setUp(self):
        super(RecurrenceMixIn, self).setUp()
        self.recurrence_start = self.get_datetime((2013, 5, 3, 21, 45))
        self.interval_start = self.get_datetime((2014, 4, 1))
        self.interval_end = self.get_datetime((2014, 4, 30))

    def test_info_renders_weekday(self):
        self.assertEqual(u'Friday every other week', self.info('biweekly'))

    def test_returns_all_dates_in_interval_for_same_weekday_every_other_week(
            self):
        self.assertEqual(
            [self.get_datetime((2014, 4, 4, 21, 45)),
             self.get_datetime((2014, 4, 18, 21, 45))],
            self.callFUT('biweekly'))
        self.assertEqual(self.recurrence_start.isoweekday(),
                         self.callFUT('biweekly')[0].isoweekday())


class DailyTests(RecurrenceMixIn, TestMixIn, unittest.TestCase):
    """Testing ..recurrence.Daily"""

    def setUp(self):
        super(RecurrenceMixIn, self).setUp()
        self.recurrence_start = self.get_datetime((2013, 5, 3, 21, 45))
        self.interval_start = self.get_datetime((2014, 4, 1))
        self.interval_end = self.get_datetime((2014, 4, 4))

    def test_info_renders_static_string(self):
        self.assertEqual(u'each day', self.info('daily'))

    def test_returns_all_dates_in_interval(self):
        self.assertEqual(
            [self.get_datetime((2014, 4, 1, 21, 45)),
             self.get_datetime((2014, 4, 2, 21, 45)),
             self.get_datetime((2014, 4, 3, 21, 45))],
            self.callFUT('daily'))


class MonthlyNthWeekdayTests(RecurrenceMixIn, TestMixIn, unittest.TestCase):
    """Testing ..recurrence.MonthlyNthWeekday"""

    def setUp(self):
        super(RecurrenceMixIn, self).setUp()
        # 3rd Thursday in month
        self.recurrence_start = self.get_datetime((2013, 3, 21, 21, 45))
        self.interval_start = self.get_datetime((2014, 4, 1, 0))
        self.interval_end = self.get_datetime((2014, 4, 30, 0))

    def test_info_renders_weekday_and_recurrence(self):
        self.assertEqual(
            u'3rd Thursday every month', self.info('nth weekday of month'))

    def test_returns_empty_interval_if_datetime_after_interval_end(self):
        self.assertEqual(
            [], self.callFUT(
                'nth weekday of month',
                datetime=self.get_datetime((2014, 5, 1, 21, 45))))

    def test_returns_all_nth_of_month_in_interval_for_same_weekday(self):
        self.assertEqual(
            [self.get_datetime((2014, 4, 17, 21, 45)),
             self.get_datetime((2014, 5, 15, 21, 45)),
             self.get_datetime((2014, 6, 19, 21, 45))],
            self.callFUT('nth weekday of month',
                         end=self.get_datetime((2014, 6, 30, 17))))
        self.assertEqual(self.recurrence_start.isoweekday(),
                         self.callFUT('nth weekday of month')[0].isoweekday())

    def test_does_not_start_before_datetime(self):
        self.assertEqual(
            [self.get_datetime((2014, 5, 4, 21, 45)),
             self.get_datetime((2014, 6, 1, 21, 45))],
            self.callFUT('nth weekday of month',
                         datetime=self.get_datetime((2014, 5, 4, 21, 45)),
                         end=self.get_datetime((2014, 6, 30, 17))))

    def test_interval_end_does_not_belong_to_interval(self):
        self.assertEqual(
            [], self.callFUT('nth weekday of month',
                             datetime=self.get_datetime((2014, 4, 30, 0))))

    def test_interval_start_belongs_to_interval(self):
        self.assertEqual(
            [self.get_datetime((2014, 4, 1, 0))],
            self.callFUT(
                'nth weekday of month',
                datetime=self.get_datetime((2014, 4, 1, 0))))

    def test_does_not_swap_into_next_month_if_month_do_not_have_a_fifth_week(
            self):
        self.assertEqual(
            [self.get_datetime((2014, 5, 31, 0)),
             self.get_datetime((2014, 8, 30, 0))],
            self.callFUT(
                'nth weekday of month',
                datetime=self.get_datetime((2014, 5, 31, 0)),
                start=self.get_datetime((2014, 5, 1, 0)),
                end=self.get_datetime((2014, 8, 31, 0))))


class BiMonthlyNthWeekdayTests(RecurrenceMixIn, TestMixIn, unittest.TestCase):
    """Testing ..recurrence.BiMonthlyNthWeekday"""

    def setUp(self):
        super(RecurrenceMixIn, self).setUp()
        # 3rd Thursday in month
        self.recurrence_start = self.get_datetime((2013, 3, 21, 21, 45))
        self.interval_start = self.get_datetime((2014, 4, 1, 0))
        self.interval_end = self.get_datetime((2014, 6, 30, 17))

    def test_info_renders_weekday_and_recurrence(self):
        self.assertEqual(u'3rd Thursday every other month',
                         self.info('nth weekday every other month'))

    def test_returns_all_nth_of_month_in_interval_every_other_month(self):
        self.assertEqual(
            [self.get_datetime((2014, 4, 17, 21, 45)),
             self.get_datetime((2014, 6, 19, 21, 45))],
            self.callFUT('nth weekday every other month'))


class MonthlyNthWeekdayFromEndTests(
        RecurrenceMixIn, TestMixIn, unittest.TestCase):
    """Testing ..recurrence.MonthlyNthWeekdayFromEnd"""

    def setUp(self):
        super(RecurrenceMixIn, self).setUp()
        # last but one Thursday in month
        self.recurrence_start = self.get_datetime((2013, 3, 21, 21, 45))
        self.interval_start = self.get_datetime((2014, 4, 1, 0))
        self.interval_end = self.get_datetime((2014, 4, 30, 0))

    def test_info_renders_weekday_and_recurrence(self):
        self.assertEqual(u'last but one Thursday every month',
                         self.info('nth weekday from end of month'))

    def test_returns_empty_interval_if_datetime_after_interval_end(self):
        self.assertEqual(
            [], self.callFUT(
                'nth weekday from end of month',
                datetime=self.get_datetime((2014, 5, 1, 21, 45))))

    def test_returns_all_nth_from_end_of_month_in_interval_for_same_weekday(
            self):
        self.assertEqual(
            [self.get_datetime((2014, 4, 17, 21, 45)),
             self.get_datetime((2014, 5, 22, 21, 45)),
             self.get_datetime((2014, 6, 19, 21, 45))],
            self.callFUT('nth weekday from end of month',
                         end=self.get_datetime((2014, 6, 30, 17))))
        self.assertEqual(
            self.recurrence_start.isoweekday(),
            self.callFUT('nth weekday from end of month')[0].isoweekday())

    def test_does_not_start_before_datetime(self):
        self.assertEqual(
            [self.get_datetime((2014, 5, 4, 21, 45)),
             self.get_datetime((2014, 6, 8, 21, 45))],
            self.callFUT('nth weekday from end of month',
                         datetime=self.get_datetime((2014, 5, 4, 21, 45)),
                         end=self.get_datetime((2014, 6, 30, 17))))

    def test_interval_end_does_not_belong_to_interval(self):
        self.assertEqual(
            [], self.callFUT('nth weekday from end of month',
                             datetime=self.get_datetime((2014, 4, 30, 0))))

    def test_interval_start_belongs_to_interval(self):
        self.assertEqual(
            [self.get_datetime((2014, 4, 1, 0))],
            self.callFUT(
                'nth weekday from end of month',
                datetime=self.get_datetime((2014, 4, 1, 0))))

    def test_does_not_swap_into_other_month_if_month_do_not_have_a_fifth_week(
            self):
        self.assertEqual(
            [self.get_datetime((2014, 5, 3, 0)),
             self.get_datetime((2014, 8, 2, 0))],
            self.callFUT(
                'nth weekday from end of month',
                datetime=self.get_datetime((2014, 5, 3, 0)),
                start=self.get_datetime((2014, 5, 1, 0)),
                end=self.get_datetime((2014, 8, 31, 0))))


class BiMonthlyNthWeekdayFromEndTests(
        RecurrenceMixIn, TestMixIn, unittest.TestCase):
    """Testing ..recurrence.BiMonthlyNthWeekdayFromEnd"""

    def setUp(self):
        super(RecurrenceMixIn, self).setUp()
        # last but one Thursday in month
        self.recurrence_start = self.get_datetime((2013, 3, 21, 21, 45))
        self.interval_start = self.get_datetime((2014, 4, 1, 0))
        self.interval_end = self.get_datetime((2014, 4, 30, 0))

    def test_info_renders_weekday_and_recurrence(self):
        self.assertEqual(u'last but one Thursday every other month',
                         self.info('nth weekday from end of other month'))

    def test_returns_all_nth_from_end_of_month_in_interval_for_same_weekday(
            self):
        self.assertEqual(
            [self.get_datetime((2014, 4, 17, 21, 45)),
             self.get_datetime((2014, 6, 19, 21, 45))],
            self.callFUT('nth weekday from end of other month',
                         end=self.get_datetime((2014, 6, 30, 17))))
        self.assertEqual(
            self.recurrence_start.isoweekday(),
            self.callFUT(
                'nth weekday from end of other month')[0].isoweekday())


class YearlyTests(RecurrenceMixIn, TestMixIn, unittest.TestCase):
    """Testing ..recurrence.Yearly"""

    def setUp(self):
        super(RecurrenceMixIn, self).setUp()
        self.recurrence_start = self.get_datetime((2013, 12, 24, 15))
        self.interval_start = self.get_datetime((2014, 1, 1))
        self.interval_end = self.get_datetime((2014, 12, 31))

    def test_info_renders_day(self):
        self.assertEqual(u'24.12. every year', self.info('yearly'))

    def test_returns_all_dates_in_interval_with_same_day_and_month(self):
        self.assertEqual(
            [self.get_datetime((2013, 12, 24, 15)),
             self.get_datetime((2014, 12, 24, 15))],
            self.callFUT('yearly', start=self.get_datetime((2012, 1, 1)),
                         end=self.get_datetime((2015, 1, 1))))

    def test_returns_empty_interval_if_datetime_after_interval_end(self):
        self.assertEqual(
            [], self.callFUT('yearly', end=self.get_datetime((2012, 5, 1))))

    def test_interval_end_does_not_belong_to_interval(self):
        self.assertEqual(
            [], self.callFUT(
                'yearly', end=self.get_datetime((2014, 12, 24, 15))))

    def test_interval_start_belongs_to_interval(self):
        self.assertEqual(
            [self.get_datetime((2014, 12, 24, 15))],
            self.callFUT(
                'yearly', start=self.get_datetime((2014, 12, 24, 15))))

    def test_handles_29th_of_february_as_28th_of_february_in_non_leap_year(
            self):
        self.assertEqual(
            [self.get_datetime((2011, 2, 28, 15)),
             self.get_datetime((2012, 2, 29, 15))],
            self.callFUT(
                'yearly', datetime=self.get_datetime((2008, 2, 29, 15)),
                start=self.get_datetime((2011, 1, 1)),
                end=self.get_datetime((2013, 1, 1))))


class NextDateOfSameWeekdayTests(unittest.TestCase, TestMixIn):
    """Testing ..recurrence.next_date_of_same_weekday()."""

    def callFUT(self, wd_src, base_date, additional_weeks=0):
        from .recurrence import next_date_of_same_weekday
        return next_date_of_same_weekday(wd_src, base_date, additional_weeks)

    def test_weekday_of_wd_src_smaller_than_weekday_of_base_date(self):
        self.assertEqual(self.get_datetime((2014, 7, 28, 10)),
                         self.callFUT(self.get_datetime((2014, 7, 21, 10)),
                                      self.get_datetime((2014, 7, 23, 10))))

    def test_weekday_of_wd_src_greater_than_weekday_of_base_date(self):
        # Weekday of 2014-07-20 is 7 (Sunday)
        self.assertEqual(self.get_datetime((2014, 7, 27, 10)),
                         self.callFUT(self.get_datetime((2014, 7, 20, 10)),
                                      self.get_datetime((2014, 7, 23, 10))))

    def test_weekday_of_wd_src_equal_to_weekday_of_base_date(self):
        self.assertEqual(self.get_datetime((2014, 7, 17, 10)),
                         self.callFUT(self.get_datetime((2014, 7, 10, 10)),
                                      self.get_datetime((2014, 7, 17, 10))))

    def test_wd_src_equal_to_base_date(self):
        dt = self.get_datetime((2014, 7, 23, 17))
        self.assertEqual(dt, self.callFUT(dt, dt))

    def test_additional_whole_weeks_can_be_added(self):
        self.assertEqual(self.get_datetime((2014, 9, 9, 15)),
                         self.callFUT(self.get_datetime((2014, 9, 2, 15)),
                                      self.get_datetime((2014, 9, 1, 15)), 1))


class RecurrencesOfWeekdayInMonthTests(unittest.TestCase, TestMixIn):
    """Tesing ..recurrence.recurrences_of_weekday_in_month()."""

    def callFUT(self, date, month):
        from .recurrence import recurrences_of_weekday_in_month
        from gocept.month import Month
        date = self.get_datetime(date)
        month = Month(*month)
        return recurrences_of_weekday_in_month(date, month)

    def test_4_recurrences_of_monday(self):
        self.assertEqual(4, self.callFUT((2014, 8, 4), (7, 2014)))

    def test_4_recurrences_of_thursday(self):
        self.assertEqual(4, self.callFUT((2014, 8, 21), (6, 2014)))

    def test_4_recurrences_of_suday(self):
        self.assertEqual(4, self.callFUT((2014, 8, 17), (7, 2014)))

    def test_5_recurrences_of_monday(self):
        self.assertEqual(5, self.callFUT((2014, 8, 4), (6, 2014)))

    def test_5_recurrences_of_thursday(self):
        self.assertEqual(5, self.callFUT((2014, 8, 21), (7, 2014)))

    def test_5_recurrences_of_sunday(self):
        self.assertEqual(5, self.callFUT((2014, 8, 17), (6, 2014)))
