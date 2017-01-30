from .interfaces import IRecurringDateTime
from datetime import timedelta, datetime
import grokcore.component as grok
import zope.interface.common.idatetime


ONE_DAY = timedelta(days=1)


def _get_isoweekday_difference(date1, date2):
    """Difference of isoweekdays between days."""
    days = 7 - (date1.isoweekday() - date2.isoweekday())
    if days >= 7:
        days -= 7
    return days


def next_date_of_same_weekday(wd_src, base_date, additional_weeks=0):
    """Compute next day with the same weekday as `wd_src` from `base_date` on.

    If `additional_weeks` is not zero, its number of weeks are added
    afterwards.
    If `wd_src` and `base_date` have the same weekday `base_date` is returned.

    """
    add_days = _get_isoweekday_difference(base_date, wd_src)
    return base_date + (add_days + additional_weeks * 7) * ONE_DAY


class RecurringDateTime(grok.Adapter):
    """Base class for recurring datestimes."""

    grok.context(zope.interface.common.idatetime.IDateTime)
    grok.implements(IRecurringDateTime)
    grok.baseclass()

    def __call__(self, interval_start, interval_end):
        self.interval_start = interval_start
        self.interval_end = interval_end
        return self.compute()

    def compute(self):
        raise NotImplementedError('Implement in subclass!')

    @property
    def _weekday(self):
        request = zope.globalrequest.getRequest()
        weekday = self.context.isoweekday()
        if request is not None:
            calendar = request.locale.dates.calendars['gregorian']
            return calendar.getDayNames()[weekday - 1]
        return weekday


class StaticIntervalBase(RecurringDateTime):
    """Base class for recurrences of a fix interval e. g. 1 day or 1 week."""

    grok.baseclass()
    interval = NotImplemented

    def _get_start_date(self):
        raise NotImplementedError('Implement in subclass!')

    def combine_with_time_of_context(self, date):
        """Combine the date with the time of the context."""
        time = self.context.time()
        tz = self.context.tzinfo
        return tz.localize(datetime.combine(date, time))

    def compute(self):
        if self.interval_start <= self.context:
            current_date = self.context
        else:
            current_date = self._get_start_date()
        while current_date < self.interval_end:
            yield self.combine_with_time_of_context(current_date)
            current_date += self.interval
