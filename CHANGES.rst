===========
 Changelog
===========

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
