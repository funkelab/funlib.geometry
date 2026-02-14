import json

import pytest

from funlib.geometry import FloatCoordinate


def test_constructor():
    # construct from tuples, lists, and generators

    assert FloatCoordinate(0) == (0,)
    assert FloatCoordinate(0, 1) == (0, 1)
    assert FloatCoordinate(0, 1, 2) == (0, 1, 2)
    assert FloatCoordinate((0, 1, 2, 3, 4, 5, 6)) == (0, 1, 2, 3, 4, 5, 6)
    assert FloatCoordinate([0, 1, 2, 3, 4, 5, 6]) == (0, 1, 2, 3, 4, 5, 6)
    assert FloatCoordinate(range(100)) == tuple(range(100))

    # preserves floats (does not convert to int)

    c = FloatCoordinate((0.1, 0.5, 1.0, 2.0))
    assert c == (0.1, 0.5, 1.0, 2.0)


def test_arithmetic():
    a = FloatCoordinate((1, 2, 3))
    b = FloatCoordinate((4, 5, 6))
    c = FloatCoordinate((7, 8))

    assert a + b == (5, 7, 9)
    assert a - b == (-3, -3, -3)
    assert b - a == (3, 3, 3)
    assert -a == (-1, -2, -3)
    assert abs(a) == a
    assert abs(-a) == a
    assert a * b == (4, 10, 18)
    assert a / b == (0.25, 0.4, 0.5)
    assert a // b == (0, 0, 0)
    assert b / a == (4.0, 2.5, 2.0)
    assert b // a == (4, 2, 2)

    assert a + 1 == (2, 3, 4)
    assert a + 1.9 == (2.9, 3.9, 4.9)
    assert a - 3 == (-2, -1, 0)
    assert a * 10 == (10, 20, 30)
    assert b / 2 == (2, 2.5, 3)
    assert b // 2 == (2, 2, 3)

    with pytest.raises(TypeError):
        a + "invalid"
    with pytest.raises(TypeError):
        a - "invalid"  # type: ignore[operator]
    with pytest.raises(TypeError):
        a * "invalid"
    with pytest.raises(TypeError):
        a / "invalid"  # type: ignore[operator]
    with pytest.raises(TypeError):
        a // "invalid"  # type: ignore[operator]
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
    a = FloatCoordinate(10, 15, 25)
    b = FloatCoordinate(5, 6, 7)

    assert a.floor_division(b) == (2, 2, 3)
    assert a.round_division(b) == (2, 2, 4)
    assert a.ceil_division(b) == (2, 3, 4)


def test_powers():
    a = FloatCoordinate(2, 3, 0)
    b = FloatCoordinate(2, 0, 1)

    assert a**b == (4, 1, 0)
    assert a**2 == (4, 9, 0)


def test_none():
    a = FloatCoordinate((None, 1, 2))
    b = FloatCoordinate((3, 4, None))

    assert a + b == (None, 5, None)
    assert a - b == (None, -3, None)
    assert a / b == (None, 0.25, None)
    assert a // b == (None, 0, None)
    assert b / a == (None, 4, None)
    assert b // a == (None, 4, None)
    assert abs(a) == (None, 1, 2)
    assert abs(-a) == (None, 1, 2)


def test_json():
    a = FloatCoordinate((1, 2, 3))
    b = FloatCoordinate((None, 2, 3))

    a_json = json.dumps(a)
    b_json = json.dumps(b)

    assert a == json.loads(a_json)
    assert b == json.loads(b_json)


def test_hash():
    assert {FloatCoordinate(1, 2, 3): "A", FloatCoordinate(4.5, 5.5, 6.5): "B"}[
        FloatCoordinate(1, 2, 3)
    ] == "A"
