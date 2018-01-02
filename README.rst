This package provides helper functions to compute recurrences of events in a
environment using the Zope Component Architecture (ZCA).

Copyright (c) 2013-2018 Michael Howitz

All Rights Reserved.

This software is subject to the provisions of the Zope Public License,
Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
FOR A PARTICULAR PURPOSE.

.. contents::

=====
Usage
=====

* Register the package at the ZCA via ZCML::

  <include package="icemac.recurrence" />

* Compute recurrences. The example computes the 2nd Tuesday each month.::

      >>> from icemac.recurrence import get_recurrences
      >>> get_recurrences(
      ...     datetime=datetime(2015, 10, 13, 11, 15),
      ...     period='nth weekday of month',
      ...     interval_start=datetime(2015, 1, 1),
      ...     interval_end=datetime(2015, 12, 31))
      [datetime(2015, 10, 13, 11, 15),
       datetime(2015, 11, 10, 11, 15),
       datetime(2015, 12, 8, 11, 15)]

* Supported recurrence periods:

  * ``daily``
  * ``weekly``
  * ``biweekly``
  * ``nth weekday of month``
  * ``nth weekday every other month``
  * ``nth weekday from end of month``
  * ``nth weekday from end of other month``
  * ``yearly``

=========
 Hacking
=========

Source code
===========

Get the source code::

   $ hg clone https://bitbucket.org/icemac/icemac.recurrence

or fork me on: https://bitbucket.org/icemac/icemac.recurrence

Running the tests
=================

To run the tests yourself call::

  $ python2.7 bootstrap.py
  $ bin/buildout -n
  $ bin/py.test
