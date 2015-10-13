import zope.interface


class IRecurringDateTime(zope.interface.Interface):
    """Recurring of a datetime.

    Period and base datetime are defined in class implementing the interface.
    """

    title = zope.interface.Attribute('Display title in RecurrencePeriodSource')
    weight = zope.interface.Attribute(
        'RecurrencePeriodSource uses `weight` to sort.')
    info = zope.interface.Attribute(
        'Information about recurrence period e. g. `every sunday`.')

    def __call__(interval_start, interval_end):
        """Iterable of recurrences of base datetime in the interval.

        interval_start, interval_end ... `datetime.date` objects

        """
