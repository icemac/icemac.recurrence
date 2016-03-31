from .interfaces import IRecurringDateTime
from .weekly import Weekly, BiWeekly
from zope.interface.verify import verifyObject
import pytest
import pytz


# Fixtures


@pytest.fixture('module')
def recurrence_start(DateTime):
    """Return default datetime when the recurrence should start."""
    return DateTime(2013, 5, 3, 21, 45)


@pytest.fixture('module')
def interval_start(DateTime):
    """Return the default start of the recurrence interval."""
    return DateTime(2014, 4, 1)


@pytest.fixture('module')
def interval_end(DateTime):
    """Return the default end of the recurrence interval."""
    return DateTime(2014, 4, 30)


# Tests


def test_weekly__Weekly__1(today):
    """It fulfills the `IRecurringDateTime` interface."""
    assert verifyObject(IRecurringDateTime, Weekly(today))


def test_weekly__Weekly__info__1(info, recurrence_start):
    """It renders the weekday."""
    assert u'Friday every week' == info(Weekly, recurrence_start)


def test_weekly__Weekly____call____1(
        DateTime, recurrence_start, interval_start, interval_end):
    """It returns all dates in the interval for same weekday."""
    result = list(Weekly(recurrence_start)(interval_start, interval_end))
    assert [
        DateTime(2014, 4, 4, 21, 45),
        DateTime(2014, 4, 11, 21, 45),
        DateTime(2014, 4, 18, 21, 45),
        DateTime(2014, 4, 25, 21, 45)] == result
    assert recurrence_start.isoweekday() == result[0].isoweekday()


def test_weekly__Weekly____call____2(DateTime, interval_start, interval_end):
    """The returned values do not start before the recurrence start."""
    dt = DateTime(2014, 4, 18, 21, 45)
    result = list(Weekly(dt)(interval_start, interval_end))
    assert [
        DateTime(2014, 4, 18, 21, 45),
        DateTime(2014, 4, 25, 21, 45)] == result
    assert dt.isoweekday() == result[0].isoweekday()


def test_weekly__Weekly____call____3(DateTime, interval_start, interval_end):
    """It returns an empty iterable if the recurrence should start after ...

    ... `interval_end`.
    """
    assert ([] == list(Weekly(
        DateTime(2014, 5, 1, 21, 45))(interval_start, interval_end)))


def test_weekly__Weekly____call____4(DateTime, recurrence_start):
    """`interval_end` does not belong to the interval."""
    assert ([] == list(Weekly(
        recurrence_start)(DateTime(2014, 4, 24), DateTime(2014, 4, 25))))


def test_weekly__Weekly____call____5(DateTime, recurrence_start):
    """`interval_start` belongs to the interval."""
    assert ([DateTime(2014, 4, 4, 21, 45)] == list(Weekly(
        recurrence_start)(DateTime(2014, 4, 4), DateTime(2014, 4, 5))))


def test_weekly__Weekly____call____6(DateTime):
    """If the context has a timezone which has DST it is respected.

    So the local time does not change if DST switches.
    DST ... daylight saving time
    """
    tz_berlin = pytz.timezone('Europe/Berlin')
    adapter = Weekly(DateTime(2016, 3, 24, 12, tzinfo=tz_berlin))
    # At 2016-03-27 DST starts in Europe/Berlin
    result = list(adapter(DateTime(2016, 3, 24, 0), DateTime(2016, 4, 1, 0)))
    assert ([DateTime(2016, 3, 24, 12, tzinfo=tz_berlin),
             DateTime(2016, 3, 31, 12, tzinfo=tz_berlin)] == result)
    # So the time in UTC changes to keep it the same in local time:
    assert ([DateTime(2016, 3, 24, 11),
             DateTime(2016, 3, 31, 10)] ==
            [pytz.utc.normalize(x) for x in result])


def test_weekly__BiWeekly__1(today):
    """It fulfills the `IRecurringDateTime` interface."""
    assert verifyObject(IRecurringDateTime, BiWeekly(today))


def test_weekly__BiWeekly____call____1(
        DateTime, recurrence_start, interval_start, interval_end):
    """returns_all_dates_in_interval_for_same_weekday_every_other_week."""
    result = list(BiWeekly(recurrence_start)(interval_start, interval_end))
    assert [
        DateTime(2014, 4, 4, 21, 45),
        DateTime(2014, 4, 18, 21, 45)] == result
    assert recurrence_start.isoweekday() == result[0].isoweekday()


def test_weekly__BiWeekly__info__1(info, recurrence_start):
    """It renders the weekday."""
    assert u'Friday every other week' == info(BiWeekly, recurrence_start)
