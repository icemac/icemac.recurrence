This package provides helper functions to compute recurrences of events in a
environment using the Zope Component Architecture (ZCA).

Copyright (c) 2013-2018 Michael Howitz

This package is licensed under the MIT License, see LICENSE.txt inside the
package.

.. image::
  https://travis-ci.com/icemac/icemac.recurrence.svg?branch=master
  :target: https://travis-ci.com/icemac/icemac.recurrence

.. image::
  https://coveralls.io/repos/github/icemac/icemac.recurrence/badge.svg
  :target: https://coveralls.io/github/icemac/icemac.recurrence

.. image:: https://img.shields.io/pypi/v/icemac.recurrence.svg
        :target: https://pypi.org/project/icemac.recurrence/
        :alt: Current version on PyPI

.. image:: https://img.shields.io/pypi/pyversions/icemac.recurrence.svg
        :target: https://pypi.org/project/icemac.recurrence/
        :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/implementation/icemac.recurrence.svg
        :target: https://pypi.org/project/icemac.recurrence/
        :alt: Supported Python implementations


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

   $ git clone https://github.com/icemac/icemac.recurrence

or fork me on: https://github.com/icemac/icemac.recurrence

Running the tests
=================

You have to install tox_ onto your machine.

To run the tests yourself call::

  $ tox

.. _tox : https://pypi.org/project/tox/
