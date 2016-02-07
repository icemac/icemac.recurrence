from .base import next_date_of_same_weekday


def test_base__next_date_of_same_weekday__1(DateTime):
    """Weekday of `wd_src` smaller than weekday of base date."""
    assert (DateTime(2014, 7, 28, 10) == next_date_of_same_weekday(
        DateTime(2014, 7, 21, 10), DateTime(2014, 7, 23, 10)))


def test_base__next_date_of_same_weekday__2(DateTime):
    """Weekday of `wd_src` greater than weekday of base date."""
    # Weekday of 2014-07-20 is 7 (Sunday)
    assert (DateTime(2014, 7, 27, 10) == next_date_of_same_weekday(
        DateTime(2014, 7, 20, 10), DateTime(2014, 7, 23, 10)))


def test_base__next_date_of_same_weekday__3(DateTime):
    """Weekday of `wd_src` equal to weekday of base date."""
    assert (DateTime(2014, 7, 17, 10) == next_date_of_same_weekday(
        DateTime(2014, 7, 10, 10), DateTime(2014, 7, 17, 10)))


def test_base__next_date_of_same_weekday__4(DateTime):
    """`wd_src` equal to base date."""
    dt = DateTime(2014, 7, 23, 17)
    assert (dt == next_date_of_same_weekday(dt, dt))


def test_base__next_date_of_same_weekday__5(DateTime):
    """Additional whole weeks can be added."""
    assert (DateTime(2014, 9, 9, 15) == next_date_of_same_weekday(
        DateTime(2014, 9, 2, 15), DateTime(2014, 9, 1, 15), 1))
