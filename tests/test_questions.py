from funlib.geometry import Coordinate as C, Roi as R
import pytest


def test_init():
    """
    Removed the need for extra parenthesis when creating Coordinates
    """
    # old behavior still works
    C((1, 2, 3))
    C(1, 2, 3)


def test_arithmetic():
    """
    Arithmetic no longer works with tuples
    """
    with pytest.raises(Exception):
        C(1, 2, 3) + (1, 2, 3)


def test_add_subtract():
    """
    Can now add/sub numbers, just like mul/div
    """
    # multiplication unchanged
    assert C(1, 2, 3) * 2 == (2, 4, 6)
    assert C(1, 2, 3) + 1 == (2, 3, 4)


def test_roi_none_args():
    """
    offset and shape can no longer be initialized as None. This may break
    gunpowder.
    """
    # Old behavior infered dimensionality of offset/shape based on
    # given shape/offset as long as one was provided
    with pytest.raises(Exception):
        R(None, C(1, 2, 3))


@pytest.mark.xfail
def test_empty_rois():
    """
    Empty roi's can (?) have a offset
    """

    assert R((1, 2, 3), (0, 0, 0)).begin == (1, 2, 3)
    assert R((0, 0, 0), (10, 10, 10)).contains(R((5, 5, 5), (0, 0, 0)))
    assert not R((0, 0, 0), (10, 10, 10)).contains(R((-1, 5, 5), (0, 0, 0)))

    # wierd cases:
    # Should a roi contain the empty roi with none offset?
    R((0, 0, 0), (10, 10, 10)).contains(R((None, None, None), (0, 0, 0)))

    # Should an empty roi contain the empty roi?
    R((None, None, None), (0, 0, 0)).contains(R((None, None, None), (0, 0, 0)))

    # what is the offset when you intersect with no overlap? Shrink more than
    # the size? Shrink exactly to zero size?
    roi1 = R((0, 0, 0), (10, 10, 10))
    roi2 = R((10, 10, 10), (10, 10, 10))
    roi3 = R((100, 100, 100), (10, 10, 10))
    assert roi1.intersect(roi2) == R((None, None, None), (0, 0, 0))
    assert roi1.intersect(roi3) == R((10, 10, 10), (0, 0, 0))
    assert roi1.grow(-6, -6) == R((None, None, None), (0, 0, 0))
    assert roi1.grow(-5, -5) == R((5, 5, 5), (0, 0, 0))


def test_roi_operations_with_tuples():
    """
    We allow passing tuples when the operation isn't ambiguous,
    e.g. grow and snap to grid
    """

    # growing with tuples
    R((0, 0, 0), (10, 10, 10)).grow((1, 2, 3), (1, 2, 3))

    # snap to grid with tuple voxel size
    R((0, 0, 0), (10, 10, 10)).snap_to_grid((4, 4, 4))
