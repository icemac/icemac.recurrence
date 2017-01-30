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


tz_berlin = pytz.timezone('Europe/Berlin')


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


def test_weekly__BiWeekly____call____1(DateTime):
    """It returns all dates in interval for same weekday every other week.

    The the recurrence does _not_ always start on the first matching week day
    in the interval.
    """
    recurrence_start = DateTime(2014, 4, 4, 21, 45)
    interval_start_1 = DateTime(2014, 5, 1)
    interval_end_1 = interval_start_2 = DateTime(2014, 5, 31)
    interval_end_2 = DateTime(2014, 6, 30)
    bi_weekly = BiWeekly(recurrence_start)
    result = list(bi_weekly(interval_start_1, interval_end_1))
    assert [
        DateTime(2014, 5, 2, 21, 45),
        DateTime(2014, 5, 16, 21, 45),
        DateTime(2014, 5, 30, 21, 45),
    ] == result
    assert recurrence_start.isoweekday() == result[0].isoweekday()
    result = list(bi_weekly(interval_start_2, interval_end_2))
    assert [
        # the first matching weekday would have been the 6th of June but this
        # date is not two weeks after the last recurrence in May, see above.
        DateTime(2014, 6, 13, 21, 45),
        DateTime(2014, 6, 27, 21, 45),
    ] == result


def test_weekly__BiWeekly____call____2(DateTime):
    """It calculates DST changes between recurrence start and interval start.

    If there is a change of the DST the recurrences are computed correctly,
    too.
    """
    recurrence_start = DateTime(2017, 1, 11, 15, 30, tzinfo=tz_berlin)
    interval_start = DateTime(2017, 4, 1, tzinfo=tz_berlin)
    interval_end = DateTime(2017, 4, 30, tzinfo=tz_berlin)
    result = list(BiWeekly(recurrence_start)(interval_start, interval_end))
    # Without DST correction the first recurrence would be on the 12th:
    assert [
        DateTime(2017, 4, 5, 15, 30, tzinfo=tz_berlin),
        DateTime(2017, 4, 19, 15, 30, tzinfo=tz_berlin),
    ] == result


def test_weekly__BiWeekly__info__1(info, recurrence_start):
    """It renders the weekday."""
    assert u'Friday every other week' == info(BiWeekly, recurrence_start)
