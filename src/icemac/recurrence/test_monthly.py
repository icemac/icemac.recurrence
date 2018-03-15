import pytz
from .interfaces import IRecurringDateTime
from .monthly import MonthlyNthWeekday, BiMonthlyNthWeekday
from .monthly import MonthlyNthWeekdayFromEnd, BiMonthlyNthWeekdayFromEnd
from .monthly import recurrences_of_weekday_in_month
from gocept.month import Month
from zope.interface.verify import verifyObject
import pytest


tz_berlin = pytz.timezone('Europe/Berlin')


# Fixtures


@pytest.fixture('module')
def recurrence_start(DateTime):
    """Return default datetime when the recurrence should start."""
    return DateTime(2013, 3, 21, 21, 45)


@pytest.fixture('module')
def interval_start(DateTime):
    """Return the default start of the recurrence interval."""
    return DateTime(2014, 4, 1, 0)


@pytest.fixture('module')
def interval_end(DateTime):
    """Return the default end of the recurrence interval."""
    return DateTime(2014, 4, 30, 0)


# Tests


def test_monthly__recurrences_of_weekday_in_month__1(DateTime):
    """There are 4 recurrences of Monday in 7/2014."""
    assert (4 == recurrences_of_weekday_in_month(
        DateTime(2014, 8, 4), Month(7, 2014)))


def test_monthly__recurrences_of_weekday_in_month__2(DateTime):
    """There are 4 recurrences of Thursday in 6/2014."""
    assert (4 == recurrences_of_weekday_in_month(
        DateTime(2014, 8, 21), Month(6, 2014)))


def test_monthly__recurrences_of_weekday_in_month__3(DateTime):
    """There are 4 recurrences of Sunday in 7/2014."""
    assert (4 == recurrences_of_weekday_in_month(
        DateTime(2014, 8, 17), Month(7, 2014)))


def test_monthly__recurrences_of_weekday_in_month__4(DateTime):
    """There are 5 recurrences of Monday in 6/2014."""
    assert (5 == recurrences_of_weekday_in_month(
        DateTime(2014, 8, 4), Month(6, 2014)))


def test_monthly__recurrences_of_weekday_in_month__5(DateTime):
    """There are 5 recurrences of Thursday in 7/2014."""
    assert (5 == recurrences_of_weekday_in_month(
        DateTime(2014, 8, 21), Month(7, 2014)))


def test_monthly__recurrences_of_weekday_in_month__6(DateTime):
    """There are 5 recurrences of Sunday in 6/2014."""
    assert (5 == recurrences_of_weekday_in_month(
        DateTime(2014, 8, 17), Month(6, 2014)))


def test_monthly__MonthlyNthWeekday__1(today):
    """It fulfills the `IRecurringDateTime` interface."""
    assert verifyObject(IRecurringDateTime, MonthlyNthWeekday(today))


def test_monthly__MonthlyNthWeekday__info__1(info, recurrence_start):
    """It renders the weekday and the recurrence."""
    assert (u'3rd Thursday every month' ==
            info(MonthlyNthWeekday, recurrence_start))


def test_monthly__MonthlyNthWeekday____call____1(
        DateTime, interval_start, interval_end):
    """It returns an empty interval if the recurrence start is after the ...

    ...interval end.
    """
    dt = DateTime(2014, 5, 1, 21, 45)
    assert [] == list(MonthlyNthWeekday(dt)(interval_start, interval_end))


def test_monthly__MonthlyNthWeekday____call____2(
        DateTime, recurrence_start, interval_start):
    """It returns all nth of month in interval for same weekday."""
    end = DateTime(2014, 6, 30, 17)
    result = list(MonthlyNthWeekday(recurrence_start)(interval_start, end))
    assert [
        DateTime(2014, 4, 17, 21, 45),
        DateTime(2014, 5, 15, 21, 45),
        DateTime(2014, 6, 19, 21, 45)] == result
    assert recurrence_start.isoweekday() == result[0].isoweekday()


def test_monthly__MonthlyNthWeekday____call____3(DateTime, interval_start):
    """It does not start before the recurrence start date."""
    dt = DateTime(2014, 5, 4, 21, 45)
    end = DateTime(2014, 6, 30, 17)
    result = list(MonthlyNthWeekday(dt)(interval_start, end))
    assert [
        DateTime(2014, 5, 4, 21, 45),
        DateTime(2014, 6, 1, 21, 45)] == result


def test_monthly__MonthlyNthWeekday____call____3_5(
        DateTime, recurrence_start, interval_end):
    """It does not start before `interval_start`."""
    start = DateTime(2014, 2, 25, 17)
    result = list(MonthlyNthWeekday(recurrence_start)(start, interval_end))
    assert [
        DateTime(2014, 3, 20, 21, 45),
        DateTime(2014, 4, 17, 21, 45),
    ] == result


def test_monthly__MonthlyNthWeekday____call____4(
        DateTime, interval_start, interval_end):
    """`interval_end` does not belong to the interval."""
    dt = DateTime(2014, 4, 30, 0)
    assert [] == list(MonthlyNthWeekday(dt)(interval_start, interval_end))


def test_monthly__MonthlyNthWeekday____call____5(
        DateTime, interval_start, interval_end):
    """`interval_start` belongs to the interval."""
    dt = DateTime(2014, 4, 1, 0)
    assert ([DateTime(2014, 4, 1, 0)] ==
            list(MonthlyNthWeekday(dt)(interval_start, interval_end)))


def test_monthly__MonthlyNthWeekday____call____6(DateTime):
    """It does not swap into the next month if the month do not have a ...

    ... fifth week.
    """
    dt = DateTime(2014, 5, 31, 0)
    start = DateTime(2014, 5, 1, 0)
    end = DateTime(2014, 8, 31, 0)
    assert [
        DateTime(2014, 5, 31, 0),
        DateTime(2014, 8, 30, 0)] == list(MonthlyNthWeekday(dt)(start, end))


def test_monthly__MonthlyNthWeekday____call____7(DateTime):
    """If the context has a timezone which has DST it is respected.

    So the local time does not change if DST switches.
    DST ... daylight saving time
    """
    adapter = MonthlyNthWeekday(DateTime(2016, 3, 24, 12, tzinfo=tz_berlin))
    # At 2016-03-27 DST starts in Europe/Berlin
    result = list(adapter(DateTime(2016, 3, 24, 0), DateTime(2016, 5, 1, 0)))
    assert ([DateTime(2016, 3, 24, 12, tzinfo=tz_berlin),
             DateTime(2016, 4, 28, 12, tzinfo=tz_berlin)] == result)
    # So the time in UTC changes to keep it the same in local time:
    assert ([DateTime(2016, 3, 24, 11),
             DateTime(2016, 4, 28, 10)] ==
            [pytz.utc.normalize(x) for x in result])


def test_monthly__BiMonthlyNthWeekday__1(today):
    """It fulfills the `IRecurringDateTime` interface."""
    assert verifyObject(IRecurringDateTime, BiMonthlyNthWeekday(today))


def test_monthly__BiMonthlyNthWeekday__info__1(info, recurrence_start):
    """It renders the weekday and the recurrence."""
    assert (u'3rd Thursday every other month' ==
            info(BiMonthlyNthWeekday, recurrence_start))


def test_monthly__BiMonthlyNthWeekday____call____1(
        DateTime, recurrence_start, interval_start):
    """It returns all nth of month in the interval every other month."""
    end = DateTime(2014, 7, 31)
    result = list(BiMonthlyNthWeekday(recurrence_start)(interval_start, end))
    assert [
        DateTime(2014, 5, 15, 21, 45),
        DateTime(2014, 7, 17, 21, 45)] == result
    assert recurrence_start.isoweekday() == result[0].isoweekday()


def test_monthly__MonthlyNthWeekdayFromEnd__1(today):
    """It fulfills the `IRecurringDateTime` interface."""
    assert verifyObject(IRecurringDateTime, MonthlyNthWeekdayFromEnd(today))


def test_monthly__MonthlyNthWeekdayFromEnd__info__1(info, recurrence_start):
    """It renders the weekday and the recurrence."""
    assert (u'last but one Thursday every month' ==
            info(MonthlyNthWeekdayFromEnd, recurrence_start))


def test_monthly__MonthlyNthWeekdayFromEnd____call____1(
        DateTime, interval_start, interval_end):
    """It returns an empty interval if the recurrence start date is after ...

    ... the interval end.
    """
    dt = DateTime(2014, 5, 1, 21, 45)
    assert ([] ==
            list(MonthlyNthWeekdayFromEnd(dt)(interval_start, interval_end)))


def test_monthly__MonthlyNthWeekdayFromEnd____call____2(
        DateTime, recurrence_start, interval_start):
    """It returns all nth from end of the month in the interval for same ...

    ... weekday.
    """
    end = DateTime(2014, 6, 30, 17)
    result = list(MonthlyNthWeekdayFromEnd(
        recurrence_start)(interval_start, end))
    assert [
        DateTime(2014, 4, 17, 21, 45),
        DateTime(2014, 5, 22, 21, 45),
        DateTime(2014, 6, 19, 21, 45)] == result
    assert recurrence_start.isoweekday() == result[0].isoweekday()


def test_monthly__MonthlyNthWeekdayFromEnd____call____3(
        DateTime, interval_start):
    """It does not start before the recurrence start date."""
    dt = DateTime(2014, 5, 4, 21, 45)
    end = DateTime(2014, 6, 30, 17)
    result = list(MonthlyNthWeekdayFromEnd(dt)(interval_start, end))
    assert [
        DateTime(2014, 5, 4, 21, 45),
        DateTime(2014, 6, 8, 21, 45)] == result


def test_monthly__MonthlyNthWeekdayFromEnd____call____4(
        DateTime, interval_start, interval_end):
    """`interval_end` does not belong to the interval."""
    dt = DateTime(2014, 4, 30, 0)
    assert ([] ==
            list(MonthlyNthWeekdayFromEnd(dt)(interval_start, interval_end)))


def test_monthly__MonthlyNthWeekdayFromEnd____call____5(
        DateTime, interval_start, interval_end):
    """`interval_start` belongs to the interval."""
    dt = DateTime(2014, 4, 1, 0)
    assert ([DateTime(2014, 4, 1, 0)] ==
            list(MonthlyNthWeekdayFromEnd(dt)(interval_start, interval_end)))


def test_monthly__MonthlyNthWeekdayFromEnd____call____6(DateTime):
    """It does not swap into the next month if the month do not have a ...

    ...fifth week.
    """
    dt = DateTime(2014, 5, 3, 0)
    start = DateTime(2014, 5, 1, 0)
    end = DateTime(2014, 8, 31, 0)
    result = list(MonthlyNthWeekdayFromEnd(dt)(start, end))
    assert [
        DateTime(2014, 5, 3, 0),
        DateTime(2014, 8, 2, 0)] == result


def test_monthly__BiMonthlyNthWeekdayFromEnd__1(today):
    """It fulfills the `IRecurringDateTime` interface."""
    assert verifyObject(IRecurringDateTime, BiMonthlyNthWeekdayFromEnd(today))


def test_monthly__BiMonthlyNthWeekdayFromEnd__info__1(info, recurrence_start):
    """It renders the weekday and the recurrence."""
    assert (u'last but one Thursday every other month' ==
            info(BiMonthlyNthWeekdayFromEnd, recurrence_start))


def test_monthly__BiMonthlyNthWeekdayFromEnd____call____1(
        DateTime, recurrence_start, interval_start):
    """It returns all nth from end of every other month in the interval for ...

    ... the same weekday.
    """
    end = DateTime(2014, 7, 31, 17)
    result = list(BiMonthlyNthWeekdayFromEnd(
        recurrence_start)(interval_start, end))
    assert [
        DateTime(2014, 5, 22, 21, 45),
        DateTime(2014, 7, 24, 21, 45)] == result
    assert recurrence_start.isoweekday() == result[0].isoweekday()


def test_monthly__BiMonthlyNthWeekdayFromEnd____call____2(DateTime):
    """It computes a correct time and time zone at DST changes.

    This is a regression test for a start date without DST and a recurrence
    with DST. Before the fix the time zone of the recurrence was without DST.
    """
    recurrence_start = DateTime(2017, 1, 31, 10, 0, tzinfo=tz_berlin)
    interval_start = DateTime(2017, 3, 1, 0, 0, tzinfo=tz_berlin)
    # DST started on 25th of March.
    interval_end = DateTime(2017, 4, 1, 0, 0, tzinfo=tz_berlin)
    result = list(BiMonthlyNthWeekdayFromEnd(
        recurrence_start)(interval_start, interval_end))
    assert [DateTime(2017, 3, 28, 10, 0, tzinfo=tz_berlin)] == result
