from .base import StaticIntervalBase, next_date_of_same_weekday
from datetime import timedelta
from icemac.recurrence.i18n import _
import grokcore.component as grok


ONE_WEEK = timedelta(days=7)
TWO_WEEKS = timedelta(days=14)


class SameWeekdayBase(StaticIntervalBase):
    """Base class for recurrences on the same weekday."""

    grok.baseclass()

    def _get_start_date(self):
        return next_date_of_same_weekday(self.context, self.interval_start)


class Weekly(SameWeekdayBase):
    """Recurring weekly on the same weekday."""

    grok.name('weekly')
    weight = 10
    title = _('weekly, same weekday (e. g. each Friday)')
    interval = ONE_WEEK

    @property
    def info(self):
        return _('${weekday} every week',
                 mapping={'weekday': self._weekday})


class BiWeekly(SameWeekdayBase):
    """Recurring biweekly on the same weekday."""

    grok.name('biweekly')
    weight = 11
    title = _('every other week, same weekday (e. g. each second Friday)')
    interval = TWO_WEEKS

    def _get_start_date(self):
        candiate = next_date_of_same_weekday(self.context, self.interval_start)
        # We have to compare the naive datetimes as otherwise the DST
        # difference might be computed into the difference of the two dates:
        naive_candiate = self.combine_with_time_of_context(
            candiate).replace(tzinfo=None)
        naive_context = self.context.replace(tzinfo=None)
        interval = (naive_candiate - naive_context).days
        assert interval % 7 == 0, \
            'Interval has {} days. This is {} weeks and {} days!'.format(
                interval, interval / 7, interval % 7)
        if interval % 14 != 0:
            # odd number of weeks
            candiate = next_date_of_same_weekday(
                self.context, self.interval_start + ONE_WEEK)
        return candiate

    @property
    def info(self):
        return _('${weekday} every other week',
                 mapping={'weekday': self._weekday})
