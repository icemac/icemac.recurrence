import datetime
import icemac.recurrence
import pytest
import pytz
import zope.configuration.xmlconfig
import zope.globalrequest
import zope.i18n
import zope.publisher.browser


@pytest.fixture(scope='session', autouse=True)
def zcmlS():
    """Load ZCML on session scope."""
    zope.configuration.xmlconfig.file('configure.zcml', icemac.recurrence)


@pytest.fixture('session')
def today():
    """Fixture returning the current day."""
    return datetime.date.today()


@pytest.fixture(scope='session')
def DateTime():
    """Fixture to ease handling of datetime objects."""
    return DateTimeClass()


class DateTimeClass:
    """Helper class to create and format datetime objects."""

    @staticmethod
    def __call__(*args, **kw):
        """Create a datetime object.

        `*args` ... time tuple parts
                    If no `args` are given the current time is returned.
        `**kw` ... the only allowed key is `tzinfo`.
                   If `tzinfo` is None, UTC is used instead.

        """
        tzinfo = kw.pop('tzinfo', pytz.utc)
        assert not kw  # make sure there are no kw left
        assert args  # make sure there is at least one argument
        return tzinfo.localize(datetime.datetime(*args))


@pytest.fixture('session')
def info():
    """Call `info` on a recurrence adapter and translate the result."""
    def info(adapter, datetime):
        request = zope.publisher.browser.TestRequest(HTTP_ACCEPT_LANGUAGE='en')
        # We have to set this request globally as otherwise the localization of
        # the weekdays returns only numbers:
        zope.globalrequest.setRequest(request)
        return zope.i18n.translate(adapter(datetime).info, request)
    return info
