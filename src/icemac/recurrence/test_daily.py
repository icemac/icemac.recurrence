from zope.interface.verify import verifyObject
from .interfaces import IRecurringDateTime
from .daily import Daily


def test_daily__Daily__1(today):
    """It fulfills the `IRecurringDateTime` interface."""
    assert verifyObject(IRecurringDateTime, Daily(today))


def test_daily__Daily____call____1(DateTime):
    """It returns all dates in the interval."""
    dt = DateTime(2013, 5, 3, 21, 45)
    start = DateTime(2014, 4, 1)
    end = DateTime(2014, 4, 4)
    assert [
        DateTime(2014, 4, 1, 21, 45),
        DateTime(2014, 4, 2, 21, 45),
        DateTime(2014, 4, 3, 21, 45)] == list(Daily(dt)(start, end))


def test_daily__Daily__info__1(info):
    """It renders a static string."""
    assert u'each day' == info(Daily, None)
