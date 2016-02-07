from .interfaces import IRecurringDateTime
import zope.component


def get_recurring(datetime, period):
    """Convenience function to get the recurring adapter named `period`."""
    return zope.component.getAdapter(datetime, IRecurringDateTime, name=period)


def get_recurrences(datetime, period, interval_start, interval_end):
    """Convenience function

    Goal: Get an interable of datetime objects of recurrences of `period`
    within the interval.

    period ... string, name of an adapter, see below
    interval_start ... date, part of the interval
    interval_end ... date, _not_ part of the interval

    """
    return get_recurring(datetime, period)(interval_start, interval_end)
