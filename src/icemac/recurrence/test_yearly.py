from .interfaces import IRecurringDateTime
from .yearly import Yearly
from zope.interface.verify import verifyObject
import pytest


# Fixtures

@pytest.fixture('module')
def recurrence_start(DateTime):
    """Return default datetime when the recurrence should start."""
    return DateTime(2013, 12, 24, 15)


@pytest.fixture('module')
def interval_start(DateTime):
    """Return the default start of the recurrence interval."""
    return DateTime(2014, 1, 1)


@pytest.fixture('module')
def interval_end(DateTime):
    """Return the default end of the recurrence interval."""
    return DateTime(2014, 12, 31)


# Tests


def test_yearly__Yearly__1(today):
    """It fulfills the `IRecurringDateTime` interface."""
    assert verifyObject(IRecurringDateTime, Yearly(today))


def test_yearly__Yearly__info__1(info, recurrence_start):
    """It renders the recurrence day."""
    assert (u'24.12. every year' == info(Yearly, recurrence_start))


def test_yearly__Yearly____call____1(DateTime, recurrence_start):
    """It returns all dates in the interval with the same day and month."""
    start = DateTime(2012, 1, 1)
    end = DateTime(2015, 1, 1)
    assert ([
        DateTime(2013, 12, 24, 15),
        DateTime(2014, 12, 24, 15)] ==
        list(Yearly(recurrence_start)(start, end)))


def test_yearly__Yearly____call____2(
        DateTime, recurrence_start, interval_start):
    """It returns an empty interval if the recurrence start is after the ...

    ... interval end.
    """
    end = DateTime(2012, 5, 1)
    assert [] == list(Yearly(recurrence_start)(interval_start, end))


def test_yearly__Yearly____call____3(
        DateTime, recurrence_start, interval_start):
    """`interval_end` does not belong to the interval."""
    end = DateTime(2014, 12, 24, 15)
    assert [] == list(Yearly(recurrence_start)(interval_start, end))


def test_yearly__Yearly____call____4(DateTime, recurrence_start, interval_end):
    """`interval_start` belongs to the interval."""
    start = DateTime(2014, 12, 24, 15)
    assert ([DateTime(2014, 12, 24, 15)] ==
            list(Yearly(recurrence_start)(start, interval_end)))


def test_yearly__Yearly____call____5(DateTime):
    """It handles the 29th of february as 28th in a non-leap year."""
    dt = DateTime(2008, 2, 29, 15)
    start = DateTime(2011, 1, 1)
    end = DateTime(2013, 1, 1)
    assert [
        DateTime(2011, 2, 28, 15),
        DateTime(2012, 2, 29, 15)] == list(Yearly(dt)(start, end))
