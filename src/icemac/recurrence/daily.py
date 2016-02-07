from icemac.recurrence.i18n import _
import grokcore.component as grok
from .base import StaticIntervalBase, ONE_DAY


class Daily(StaticIntervalBase):
    """Recurring each day."""

    grok.name('daily')
    weight = 5
    interval = ONE_DAY
    title = _('daily')
    info = _('each day')

    def _get_start_date(self):
        return self.interval_start
