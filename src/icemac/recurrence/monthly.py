from .base import RecurringDateTime
from .base import next_date_of_same_weekday, _get_isoweekday_difference
from datetime import datetime
from icemac.recurrence.i18n import _
import gocept.month
import grokcore.component as grok
import math
import zope.cachedescriptors.property


def recurrences_of_weekday_in_month(date, month):
    """Return number of recurrences of weekday of `date` in `month`."""
    minus_days = _get_isoweekday_difference(month.firstOfMonth(), date)
    return int(math.ceil((month.lastOfMonth().day - minus_days) / 7.0))


class SameNthWeekdayInMonthBase(RecurringDateTime):
    """Base class for recurrings on the same day nth weekday in month."""

    grok.baseclass()
    month_interval = NotImplemented
    n = NotImplemented

    def compute(self):
        if self.context > self.interval_end:
            return  # no need to compute: there will be no results
        self.current_month = gocept.month.IMonth(self.interval_start.date())
        # Adjust self.current_month to a multiple of self.month_interval:
        interval_len = len(
            self.current_month - gocept.month.IMonth(self.context.date()))
        # We have to substract 1 because a month interval with the same month
        # as start and end has a len of 1 but we need it zero based here:
        self.current_month += (interval_len - 1) % self.month_interval

        time = self.context.time()
        tz = self.context.tzinfo
        while True:
            result = tz.localize(next_date_of_same_weekday(
                self.context,
                datetime.combine(self.current_month.firstOfMonth(), time),
                self.n))
            try:
                if result.month != self.current_month.month:
                    continue  # result has swapped into next month
            finally:
                self.current_month += self.month_interval
            if result >= self.interval_end:
                break
            if result < self.context:
                continue
            if result < self.interval_start:
                continue
            yield result


class SameNthWeekdayFromBeginningInMonthBase(SameNthWeekdayInMonthBase):
    """Base class

    For recurrings on the same day nth weekday in month counting from the
    beginning of the month.
    """

    grok.baseclass()

    n_mapping = {0: _('1st'),
                 1: _('2nd'),
                 2: _('3rd'),
                 3: _('4th'),
                 4: _('5th')}

    @zope.cachedescriptors.property.Lazy
    def n(self):
        return int(math.ceil(self.context.day / 7.0)) - 1

    @property
    def info(self):
        return _(self.message_id,
                 mapping={'recurrence': self.n_mapping[self.n],
                          'weekday': self._weekday})


class MonthlyNthWeekday(SameNthWeekdayFromBeginningInMonthBase):
    """Recurring monthly on same recurrence of the weekday in the month as ...

    ... in `self.context`.
    """

    grok.name('nth weekday of month')
    weight = 20
    title = _('monthly, same weekday (e. g. each 3rd Sunday)')
    month_interval = 1
    message_id = _('${recurrence} ${weekday} every month')


class BiMonthlyNthWeekday(SameNthWeekdayFromBeginningInMonthBase):
    """Recurring monthly on same recurrence of the weekday in the month as ...

    ... in `self.context` but only every other month.
    """

    grok.name('nth weekday every other month')
    weight = 25
    title = _('every other month, same weekday '
              '(e. g. each 3rd Sunday in other month)')
    month_interval = 2
    message_id = _('${recurrence} ${weekday} every other month')


class SameNthWeekdayFromEndInMonthBase(SameNthWeekdayInMonthBase):
    """Base class for recurrings on the same day nth weekday in month ...

    ... counting from the end of the month.
    """

    grok.baseclass()

    n_mapping = {1: _('last'),
                 2: _('last but one'),
                 3: _('last but two'),
                 4: _('last but three'),
                 5: _('last but four')}

    @zope.cachedescriptors.property.Lazy
    def n_from_end(self):
        last_of_month = gocept.month.IMonth(self.context).lastOfMonth()
        return int(
            math.ceil((last_of_month.day - (self.context.day - 1)) / 7.0))

    @property
    def n(self):
        return recurrences_of_weekday_in_month(
            self.context, self.current_month) - self.n_from_end

    @property
    def info(self):
        return _(self.message_id,
                 mapping={'recurrence': self.n_mapping[self.n_from_end],
                          'weekday': self._weekday})


class MonthlyNthWeekdayFromEnd(SameNthWeekdayFromEndInMonthBase):
    """Recurring monthly on same recurrence of the weekday in the month as ...

    ... in `self.context`.
    """

    grok.name('nth weekday from end of month')
    weight = 21
    title = _('monthly, same weekday counted from the end of the month '
              '(e. g. each last but one Sunday)')
    month_interval = 1
    message_id = _('${recurrence} ${weekday} every month')


class BiMonthlyNthWeekdayFromEnd(SameNthWeekdayFromEndInMonthBase):
    """Recurring monthly on same recurrence of the weekday in the month as ...

    ... in `self.context` but only each other month.
    """

    grok.name('nth weekday from end of other month')
    weight = 26
    title = _('every other month on same weekday counted from the end of the '
              'month (e. g. each last but one Sunday every other month)')
    month_interval = 2
    message_id = _('${recurrence} ${weekday} every other month')
