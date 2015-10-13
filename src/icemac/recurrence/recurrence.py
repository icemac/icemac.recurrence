from datetime import timedelta, datetime
from icemac.recurrence.i18n import _
import gocept.month
import grokcore.component as grok
import icemac.recurrence.interfaces
import math
import zope.cachedescriptors.property
import zope.component
import zope.globalrequest
import zope.interface.common.idatetime


ONE_DAY = timedelta(days=1)
ONE_WEEK = timedelta(days=7)
TWO_WEEKS = timedelta(days=14)


def get_recurring(datetime, period):
    """Convenience function to get the recurring adapter named `period`."""
    return zope.component.getAdapter(
        datetime, icemac.recurrence.interfaces.IRecurringDateTime,
        name=period)


def get_recurrences(datetime, period, interval_start, interval_end):
    """Convenience function

    Goal: Get an interable of datetime objects of recurrences of `period`
    within the interval.

    period ... string, name of an adapter, see below
    interval_start ... date, part of the interval
    interval_end ... date, _not_ part of the interval

    """
    return get_recurring(datetime, period)(interval_start, interval_end)


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


def recurrences_of_weekday_in_month(date, month):
    """Return number of recurrences of weekday of `date` in `month`."""
    minus_days = _get_isoweekday_difference(month.firstOfMonth(), date)
    return int(math.ceil((month.lastOfMonth().day - minus_days) / 7.0))


def add_years(date, years):
    """Add `years` number of years to date."""
    try:
        return date.replace(year=date.year + years)
    except ValueError:
        # Handle 29th of february as 28th in non-leap years:
        return date.replace(year=date.year + years, day=date.day - 1)


class RecurringDateTime(grok.Adapter):
    """Base class for recurring datestimes."""

    grok.context(zope.interface.common.idatetime.IDateTime)
    grok.implements(icemac.recurrence.interfaces.IRecurringDateTime)
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

    def compute(self):
        if self.interval_start <= self.context:
            current_date = self.context
        else:
            current_date = self._get_start_date()
        time = self.context.timetz()
        while current_date < self.interval_end:
            yield datetime.combine(current_date, time)
            current_date += self.interval


class Daily(StaticIntervalBase):
    """Recurring each day."""

    grok.name('daily')
    weight = 5
    interval = ONE_DAY
    title = _('daily')
    info = _('each day')

    def _get_start_date(self):
        return self.interval_start


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

    @property
    def info(self):
        return _('${weekday} every other week',
                 mapping={'weekday': self._weekday})


class SameNthWeekdayInMonthBase(RecurringDateTime):
    """Base class for recurrings on the same day nth weekday in month."""

    grok.baseclass()
    month_interval = NotImplemented
    n = NotImplemented

    def compute(self):
        if self.context > self.interval_end:
            return  # no need to compute: there will be no results
        self.current_month = gocept.month.IMonth(self.interval_start.date())
        time = self.context.timetz()
        while True:
            result = next_date_of_same_weekday(
                self.context,
                datetime.combine(self.current_month.firstOfMonth(), time),
                self.n)
            try:
                if result.month != self.current_month.month:
                    continue  # result has swapped into next month
            finally:
                self.current_month += self.month_interval
            if result >= self.interval_end:
                break
            if result < self.context:
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
    """Recurring monthly on same recurrence of the weekday in the month as in
    `self.context`.
    """

    grok.name('nth weekday of month')
    weight = 20
    title = _('monthly, same weekday (e. g. each 3rd Sunday)')
    month_interval = 1
    message_id = _('${recurrence} ${weekday} every month')


class BiMonthlyNthWeekday(SameNthWeekdayFromBeginningInMonthBase):
    """Recurring monthly on same recurrence of the weekday in the month as in
    `self.context` but only every other month.
    """

    grok.name('nth weekday every other month')
    weight = 25
    title = _('every other month, same weekday '
              '(e. g. each 3rd Sunday in other month)')
    month_interval = 2
    message_id = _('${recurrence} ${weekday} every other month')


class SameNthWeekdayFromEndInMonthBase(SameNthWeekdayInMonthBase):
    """Base class for recurrings on the same day nth weekday in month counting
    from the end of the month."""

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
    """Recurring monthly on same recurrence of the weekday in the month as in
    `self.context`.
    """

    grok.name('nth weekday from end of month')
    weight = 21
    title = _('monthly, same weekday counted from the end of the month '
              '(e. g. each last but one Sunday)')
    month_interval = 1
    message_id = _('${recurrence} ${weekday} every month')


class BiMonthlyNthWeekdayFromEnd(SameNthWeekdayFromEndInMonthBase):
    """Recurring monthly on same recurrence of the weekday in the month as in
    `self.context` but only each other month.
    """

    grok.name('nth weekday from end of other month')
    weight = 26
    title = _('every other month on same weekday counted from the end of the '
              'month (e. g. each last but one Sunday every other month)')
    month_interval = 2
    message_id = _('${recurrence} ${weekday} every other month')


class Yearly(RecurringDateTime):
    """Recurring on the same date each year."""

    grok.name('yearly')
    weight = 100
    title = _('yearly (e. g. 24th of December)')

    def compute(self):
        if self.context > self.interval_end:
            return  # no need to compute: there will be no results
        date = self.context
        index = 0
        while date < self.interval_start:
            index += 1
            date = add_years(self.context, index)
        while date < self.interval_end:
            yield date
            index += 1
            date = add_years(self.context, index)

    @property
    def info(self):
        return _('${date} every year',
                 mapping={'date': self.context.strftime('%d.%m.')})
