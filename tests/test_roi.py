import pytest

from funlib.geometry import Coordinate as Coord
from funlib.geometry import Roi


def test_squeeze():
    r = Roi((1, 2, 3), (4, 5, 6))
    assert r.dims == 3
    r = r.squeeze(1)
    assert r.dims == 2

    assert r == Roi((1, 3), (4, 6))


def test_offset_and_shape_dims_must_match():
    with pytest.raises(AssertionError):
        Roi((0,), (1, 2, 3))


@pytest.mark.parametrize(
    "roi, size, empty, unbounded",
    [
        (Roi((0,), (1,)), 1, False, False),
        (Roi((0,), (0,)), 0, True, False),
        (Roi((0,), (None,)), None, False, True),
    ],
)
def test_size_empty_unbounded(roi, size, empty, unbounded):
    assert roi.size == size
    assert roi.empty is empty
    assert roi.unbounded is unbounded


def test_set_shape_and_offset():
    # unbounded ROI: the offset of an unbounded dimension is None
    r = Roi((0,), (None,))
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


def test_equality():
    assert Roi((0, 0, 0), (100, 100, 100)) == Roi((0, 0, 0), (100, 100, 100))
    assert Roi((0, 0, 0), (100, 100, 100)) != Roi((50, 50, 50), (100, 100, 100))


@pytest.mark.parametrize(
    "roi, center",
    [
        (Roi((0, 0, 0), (100, 100, 100)), (50, 50, 50)),
        (Roi((50, 50, 50), (100, 100, 100)), (100, 100, 100)),
    ],
)
def test_center(roi, center):
    assert roi.center == center


@pytest.mark.parametrize(
    "a, b, expected",
    [
        # overlapping
        (Roi((0, 0, 0), (100, 100, 100)), Roi((50, 50, 50), (100, 100, 100)), True),
        (Roi((50, 50, 50), (100, 100, 100)), Roi((0, 0, 0), (100, 100, 100)), True),
        (Roi((0, 0, 0), (100, 100, 100)), Roi((0, 0, 0), (1, 1, 1)), True),
        # unbounded
        (Roi((0, 0, 0), (100, 100, 100)), Roi((None,) * 3, (None,) * 3), True),
        # touching
        (Roi((0, 0, 0), (100, 100, 100)), Roi((100, 100, 100), (1, 1, 1)), False),
        # empty
        (Roi((0, 0, 0), (100, 100, 100)), Roi((0, 0, 0), (0, 0, 0)), False),
    ],
)
def test_intersects(a, b, expected):
    assert a.intersects(b) is expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (
            Roi((0, 0, 0), (100, 100, 100)),
            Roi((50, 50, 50), (100, 100, 100)),
            Roi((50, 50, 50), (50, 50, 50)),
        ),
        (
            Roi((50, 50, 50), (100, 100, 100)),
            Roi((0, 0, 0), (100, 100, 100)),
            Roi((50, 50, 50), (50, 50, 50)),
        ),
        # one dimension unbounded
        (
            Roi((0, None, 0), (100, None, 100)),
            Roi((50, 50, 50), (100, 100, 100)),
            Roi((50, 50, 50), (50, 100, 50)),
        ),
        (
            Roi((50, 50, 50), (100, 100, 100)),
            Roi((0, None, 0), (100, None, 100)),
            Roi((50, 50, 50), (50, 100, 50)),
        ),
        # no overlap: the empty ROI has no offset
        (
            Roi((0, 0, 0), (100, 100, 100)),
            Roi((100, 100, 100), (1, 1, 1)),
            Roi((None, None, None), (0, 0, 0)),
        ),
    ],
)
def test_intersect(a, b, expected):
    assert a.intersect(b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (
            Roi((0, 0, 0), (100, 100, 100)),
            Roi((50, 50, 50), (100, 100, 100)),
            Roi((0, 0, 0), (150, 150, 150)),
        ),
        (
            Roi((50, 50, 50), (100, 100, 100)),
            Roi((0, 0, 0), (100, 100, 100)),
            Roi((0, 0, 0), (150, 150, 150)),
        ),
        # one dimension unbounded
        (
            Roi((0, None, 0), (100, None, 100)),
            Roi((50, 50, 50), (100, 100, 100)),
            Roi((0, None, 0), (150, None, 150)),
        ),
        (
            Roi((50, 50, 50), (100, 100, 100)),
            Roi((0, None, 0), (100, None, 100)),
            Roi((0, None, 0), (150, None, 150)),
        ),
    ],
)
def test_union(a, b, expected):
    assert a.union(b) == expected


@pytest.mark.parametrize(
    "roi, other, expected",
    [
        # a ROI
        (Roi((0, 0, 0), (100, 100, 100)), Roi((25, 25, 25), (50, 50, 50)), True),
        (Roi((50, 50, 50), (100, 100, 100)), Roi((25, 25, 25), (50, 50, 50)), False),
        # a coordinate
        (Roi((0, 0, 0), (100, 100, 100)), Coord(50, 50, 50), True),
        # one dimension unbounded
        (Roi((0, None, 0), (100, None, 100)), Roi((25, 25, 25), (50, 50, 50)), True),
        (Roi((0, None, 0), (100, None, 100)), Roi((None,) * 3, (None,) * 3), False),
        # an empty ROI is contained when its offset is
        (Roi((0, None, 0), (100, None, 100)), Roi((0, 0, 0), (0, 0, 0)), True),
        (Roi((0, 0, 0), (10, 10, 10)), Roi((5, 5, 5), (0, 0, 0)), True),
        (Roi((0, 0, 0), (10, 10, 10)), Roi((-1, 5, 5), (0, 0, 0)), False),
        # an empty ROI contains the empty ROI
        (
            Roi((None, None, None), (0, 0, 0)),
            Roi((None, None, None), (0, 0, 0)),
            True,
        ),
    ],
)
def test_contains(roi, other, expected):
    assert roi.contains(other) is expected


@pytest.mark.parametrize(
    "roi, amount_neg, amount_pos, expected",
    [
        (
            Roi((0, None, 0), (100, None, 100)),
            Coord(1, 1, 1),
            Coord(1, 1, 1),
            Roi((-1, None, -1), (102, None, 102)),
        ),
        (
            Roi((0, None, 0), (100, None, 100)),
            -1,
            -1,
            Roi((1, None, 1), (98, None, 98)),
        ),
        (Roi((0, None, 0), (100, None, 100)), -1, 0, Roi((1, None, 1), (99, None, 99))),
        (
            Roi((0, None, 0), (100, None, 100)),
            0,
            Coord(-1, -1, -1),
            Roi((0, None, 0), (99, None, 99)),
        ),
        # tuples
        (
            Roi((0, 0, 0), (10, 10, 10)),
            (1, 2, 3),
            (1, 2, 3),
            Roi((-1, -2, -3), (12, 14, 16)),
        ),
        # shrinking to zero size keeps the offset
        (Roi((0, 0, 0), (10, 10, 10)), -5, -5, Roi((5, 5, 5), (0, 0, 0))),
    ],
)
def test_grow(roi, amount_neg, amount_pos, expected):
    assert roi.grow(amount_neg, amount_pos) == expected


@pytest.mark.parametrize(
    "roi, voxel_size, mode, expected",
    [
        (Roi((1,), (7,)), Coord(2), "grow", Roi((0,), (8,))),
        (Roi((1,), (7,)), Coord(2), "shrink", Roi((2,), (6,))),
        (Roi((1,), (7,)), Coord(2), "closest", Roi((0,), (8,))),
        (Roi((1,), (7,)), Coord(3), "grow", Roi((0,), (9,))),
        (Roi((1,), (7,)), Coord(3), "shrink", Roi((3,), (3,))),
        (Roi((1,), (7,)), Coord(3), "closest", Roi((0,), (9,))),
        # one dimension unbounded
        (Roi((1, None), (7, None)), Coord(2, 1), "grow", Roi((0, None), (8, None))),
        # negative offset, already on the grid
        (Roi((-20,), (2,)), Coord(2), "shrink", Roi((-20,), (2,))),
        # tuple voxel size
        (Roi((0, 0, 0), (10, 10, 10)), (4, 4, 4), "grow", Roi((0, 0, 0), (12, 12, 12))),
    ],
)
def test_snap_to_grid(roi, voxel_size, mode, expected):
    assert roi.snap_to_grid(voxel_size, mode) == expected


def test_snap_to_grid_unknown_mode():
    with pytest.raises(RuntimeError):
        Roi((1, None), (7, None)).snap_to_grid(Coord(3, 1), "doesntexist")


def test_arithmetic():
    a = Roi((1, None), (7, None))

    assert a + 1 == Roi((2, None), (7, None))
    assert a - 1 == Roi((0, None), (7, None))
    assert a * 2 == Roi((2, None), (14, None))
    assert a / 2 == Roi((0, None), (3, None))
    assert a // 2 == Roi((0, None), (3, None))
