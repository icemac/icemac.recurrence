import plone.testing.zca
import icemac.recurrence
import pytest


@pytest.yield_fixture(scope='session', autouse=True)
def zcmlS():
    """Load ZCML on session scope."""
    layer = plone.testing.zca.ZCMLSandbox(
        name="RecurrenceZCML", bases=[], filename="configure.zcml",
        module=__name__, package=icemac.recurrence)
    layer.setUp()
    yield layer['configurationContext']
    layer.tearDown()
