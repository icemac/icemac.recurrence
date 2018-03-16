===========
 Changelog
===========

1.4.2 (2018-03-16)
==================

- Fix the computation of monthly recurrences not to return a date before the
  given `interval_start` date.


1.4.1.post1 (2017-12-26)
========================

- Also release as wheel.


1.4.1 (2017-04-11)
==================

- Fix a corner case in the computation of monthly recurrences: If the
  beginning of the interval for which recurrences should be computed was
  outside DST but the recurrence date was inside DST - it was incorrectly
  returned with a time zone object which did not have DST switched on.


1.4 (2017-04-08)
================

- No longer exclude tests from coverage report.


1.3.1 (2017-02-04)
==================

- Fix computation of biweekly recurrences: Previously the first recurrence with
  a matching weekday in the interval was used as the first result for the
  interval. This is only correct in half of the cases. Now the computation of
  the first recurrence in the interval takes into account that it has to be an
  even number of weeks after the recurrence start date and it handles DST
  differences correctly.


1.3 (2017-01-07)
================

- Add Manifest and clean up coverage configuration.


1.2 (2016-04-16)
================

- Fix handling for dates with a timezone which has a daylight saving time
  (DST): The local time of the recurrence does not change when switching DST
  though the UTC representation of the time will now change.


1.1 (2016-03-01)
================

- Shorten the import path of ``get_recurrences()`` from
  ``icemac.recurrence.recurrence`` to just ``icemac.recurrence``.

- Refactor tests to use ``py.test`` fixtures.

- Fix an off by one month error in the periods `nth weekday every other month`
  and `nth weekday from end of other month`.

- Bring the test coverage to 100 % even in branch coverage.


1.0.1 (2015-10-22)
==================

- Fix broken 1.0.0 release.


1.0.0 (2015-10-13)
==================

* Extract package from `icemac.ab.calendar` for reuse in other projects.
