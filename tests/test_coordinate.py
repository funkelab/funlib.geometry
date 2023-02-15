import pytest

from funlib.geometry import Coordinate


def test_constructor():

    # construct from tuples, lists, and generators

    assert Coordinate(0) == (0,)
    assert Coordinate(0, 1) == (0, 1)
    assert Coordinate(0, 1, 2) == (0, 1, 2)
    assert Coordinate((0, 1, 2, 3, 4, 5, 6)) == (0, 1, 2, 3, 4, 5, 6)
    assert Coordinate([0, 1, 2, 3, 4, 5, 6]) == (0, 1, 2, 3, 4, 5, 6)
    assert Coordinate(range(100)) == tuple(range(100))

    # convert to integer

    c = Coordinate((0.1, 0.5, 1.0, 2.0))
    assert c == (0, 0, 1, 2)


def test_arithmetic():

    a = Coordinate((1, 2, 3))
    b = Coordinate((4, 5, 6))
    c = Coordinate((7, 8))

    assert a + b == (5, 7, 9)
    assert a - b == (-3, -3, -3)
    assert b - a == (3, 3, 3)
    assert -a == (-1, -2, -3)
    assert abs(a) == a
    assert abs(-a) == a
    assert a * b == (4, 10, 18)
    assert a / b == (0, 0, 0)
    assert a // b == (0, 0, 0)
    assert b / a == (4, 2, 2)
    assert b // a == (4, 2, 2)

    assert a + 1 == (2, 3, 4)
    assert a + 1.9 == (2, 3, 4)
    assert a - 3 == (-2, -1, 0)
    assert a * 10 == (10, 20, 30)
    assert b / 2 == (2, 2, 3)
    assert b // 2 == (2, 2, 3)

    with pytest.raises(TypeError):
        a + "invalid"
    with pytest.raises(TypeError):
        a - "invalid"
    with pytest.raises(TypeError):
        a * "invalid"
    with pytest.raises(TypeError):
        a / "invalid"
    with pytest.raises(TypeError):
        a // "invalid"
    with pytest.raises(AssertionError):
        a + c
    with pytest.raises(AssertionError):
        a - c
    with pytest.raises(AssertionError):
        a * c
    with pytest.raises(AssertionError):
        a / c
    with pytest.raises(AssertionError):
        a // c


def test_division():
    a = Coordinate(10, 15, 25)
    b = Coordinate(5, 6, 7)

    assert a.floor_division(b) == (2, 2, 3)
    assert a.round_division(b) == (2, 2, 4)
    assert a.ceil_division(b) == (2, 3, 4)


def test_powers():
    a = Coordinate(2, 3, 0)
    b = Coordinate(2, 0, 1)

    assert a ** b == (4, 1, 0)
    assert a ** 2 == (4, 9, 0)


def test_none():

    a = Coordinate((None, 1, 2))
    b = Coordinate((3, 4, None))

    assert a + b == (None, 5, None)
    assert a - b == (None, -3, None)
    assert a / b == (None, 0, None)
    assert a // b == (None, 0, None)
    assert b / a == (None, 4, None)
    assert b // a == (None, 4, None)
    assert abs(a) == (None, 1, 2)
    assert abs(-a) == (None, 1, 2)
