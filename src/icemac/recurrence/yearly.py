from .base import RecurringDateTime
from icemac.recurrence.i18n import _
import grokcore.component as grok


def add_years(date, years):
    """Add `years` number of years to date."""
    try:
        return date.replace(year=date.year + years)
    except ValueError:
        # Handle 29th of February as 28th in non-leap years:
        return date.replace(year=date.year + years, day=date.day - 1)


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
        # Find first date after interval_start:
        while date < self.interval_start:
            index += 1
            date = add_years(self.context, index)
        # Yield dates in the interval:
        while date < self.interval_end:
            yield date
            index += 1
            date = add_years(self.context, index)

    @property
    def info(self):
        return _('${date} every year',
                 mapping={'date': self.context.strftime('%d.%m.')})
