from funlib.geometry import Roi
from funlib.geometry import Coordinate as Coord
import pytest


def test_squeeze():

    r = Roi((1, 2, 3), (4, 5, 6))
    assert r.dims == 3
    r = r.squeeze(1)
    assert r.dims == 2

    assert r == Roi((1, 3), (4, 6))


def test_shape():

    r = Roi((0,), (1,))
    assert r.size == 1
    assert r.empty is False
    assert r.unbounded is False

    r = Roi((0,), (0,))
    assert r.size == 0
    assert r.empty is True
    assert r.unbounded is False

    # unbounded ROI
    r = Roi((0,), (None,))
    assert r.size is None
    assert r.empty is False
    assert r.unbounded is True
    assert r.offset == (None,)
    assert r.end == (None,)
    assert r.shape == (None,)
    r.offset = (1,)
    assert r.offset == (None,)
    assert r.end == (None,)
    assert r.shape == (None,)

    # turn into bounded ROI without offset
    r.shape = (3,)
    assert r.offset == (None,)
    assert r.end == (None,)
    assert r.shape == (3,)

    # turn into regular ROI
    r.offset = (1,)
    assert r.offset == (1,)
    assert r.end == (4,)
    assert r.shape == (3,)
    assert r.size == 3

    # turn back into unbounded ROI
    r.shape = None
    assert r.dims == 1
    assert r.offset == (None,)
    assert r.end == (None,)
    assert r.shape == (None,)
    assert r.size is None


def test_operators():

    a = Roi((0, 0, 0), (100, 100, 100))
    b = Roi((50, 50, 50), (100, 100, 100))

    assert a != b
    assert a.intersects(b)
    assert b.intersects(a)
    assert a.intersects(Roi((None,) * 3, (None,) * 3))
    assert a.intersects(Roi((0, 0, 0), (1, 1, 1)))
    assert not a.intersects(Roi((0, 0, 0), (0, 0, 0)))
    assert a.intersect(Roi((100, 100, 100), (1, 1, 1))).empty

    assert a.center == (50, 50, 50)
    assert b.center == (100, 100, 100)

    assert a.intersect(b) == Roi((50, 50, 50), (50, 50, 50))
    assert b.intersect(a) == Roi((50, 50, 50), (50, 50, 50))
    assert a.union(b) == Roi((0, 0, 0), (150, 150, 150))
    assert b.union(a) == Roi((0, 0, 0), (150, 150, 150))

    c = Roi((25, 25, 25), (50, 50, 50))

    assert a.contains(c)
    assert a.contains(c.center)
    assert not b.contains(c)

    a = Roi((0, None, 0), (100, None, 100))
    b = Roi((50, 50, 50), (100, 100, 100))

    assert a.intersect(b) == Roi((50, 50, 50), (50, 100, 50))
    assert b.intersect(a) == Roi((50, 50, 50), (50, 100, 50))
    assert a.union(b) == Roi((0, None, 0), (150, None, 150))
    assert b.union(a) == Roi((0, None, 0), (150, None, 150))

    c = Roi((25, 25, 25), (50, 50, 50))

    assert a.contains(c)
    assert not b.contains(c)
    assert a.contains(Roi((0, 0, 0), (0, 0, 0)))
    # assert b.contains(Roi((0, 0, 0), (0, 0, 0)))
    assert not a.contains(Roi((None,) * 3, (None,) * 3))

    assert a.grow(Coord(1, 1, 1), Coord(1, 1, 1)) == Roi(
        (-1, None, -1), (102, None, 102)
    )
    assert a.grow(-1, -1) == Roi((1, None, 1), (98, None, 98))
    assert a.grow(-1, 0) == Roi((1, None, 1), (99, None, 99))
    assert a.grow(amount_pos=Coord(-1, -1, -1)) == Roi((0, None, 0), (99, None, 99))


def test_snap():

    a = Roi((1,), (7,))

    assert a.snap_to_grid(Coord(2), "grow") == Roi((0,), (8,))
    assert a.snap_to_grid(Coord(2), "shrink") == Roi((2,), (6,))
    assert a.snap_to_grid(Coord(2), "closest") == Roi((0,), (8,))

    assert a.snap_to_grid(Coord(3), "grow") == Roi((0,), (9,))
    assert a.snap_to_grid(Coord(3), "shrink") == Roi((3,), (3,))
    assert a.snap_to_grid(Coord(3), "closest") == Roi((0,), (9,))

    a = Roi((1, None), (7, None))
    assert a.snap_to_grid(Coord(2, 1), "grow") == Roi((0, None), (8, None))

    with pytest.raises(RuntimeError):
        a.snap_to_grid(Coord(3, 1), "doesntexist")

    r = Roi((-20,), (2,))
    c = Coord(
        2,
    )
    assert not r.snap_to_grid(c, mode="shrink").empty, (
        f"begin: {(r.begin, r.begin.ceil_division(c))}, "
        f"end: {(r.end, r.end.floor_division(c))}"
    )


def test_arithmetic():

    a = Roi((1, None), (7, None))

    assert a + 1 == Roi((2, None), (7, None))
    assert a - 1 == Roi((0, None), (7, None))
    assert a * 2 == Roi((2, None), (14, None))
    assert a / 2 == Roi((0, None), (3, None))
    assert a // 2 == Roi((0, None), (3, None))
