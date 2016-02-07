from .recurrence import get_recurring, get_recurrences
from .weekly import Weekly
from zope.component import ComponentLookupError
import collections
import pytest


def test_recurrence__get_recurring__1(DateTime):
    """It returns the named recurrence adapter."""
    assert Weekly == get_recurring(DateTime(2016, 2, 6), 'weekly').__class__


def test_recurrence__get_recurring__2(DateTime):
    """It raises a TypeError if there is no adapter registered for the name."""
    with pytest.raises(ComponentLookupError):
        get_recurring(DateTime(2016, 2, 6), 'foobar')


def test_recurrence__get_recurrences__1(DateTime):
    """It returns an iterable of datetime objects."""
    dt = DateTime(2016, 2, 6, 10)
    start = DateTime(2016, 3, 1)
    end = DateTime(2016, 6, 30)
    result = get_recurrences(
        dt, 'nth weekday from end of other month', start, end)
    assert isinstance(result, collections.Iterable)
    assert [DateTime(2016, 4, 9, 10),
            DateTime(2016, 6, 4, 10)] == list(result)
