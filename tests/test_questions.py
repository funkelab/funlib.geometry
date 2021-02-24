from funlib.geometry import Coordinate as C, Roi as R
import pytest


def test_init():
    """
    Removed the need for extra parenthesis when creating Coordinates
    """
    # old behavior still works
    C((1, 2, 3))
    with pytest.raises(Exception):
        C(1, 2, 3)


def test_arithmetic():
    """
    Arithmetic no longer works with tuples
    """
    C(1, 2, 3) + (1, 2, 3)


def test_add_subtract():
    """
    Can now add/sub numbers, just like mul/div
    """
    # multiplication unchanged
    assert C(1, 2, 3) * 2 == (2, 4, 6)
    with pytest.raises(Exception):
        C(1, 2, 3) + 1 == (2, 3, 4)


def test_roi_none_args():
    """
    offset and shape can no longer be initialized as None
    """
    # Old behavior infered dimensionality of offset/shape based on
    # given shape/offset as long as one was provided
    R(None, C(1, 2, 3))


def test_empty_rois():
    """
    Empty roi's can no longer have a offset
    """

    assert R((1, 2, 3), (0, 0, 0)).get_begin() == (None, None, None)

    # This no longer works:
    assert R((0, 0, 0), (10, 10, 10)).contains(R((5, 5, 5), (0, 0, 0)))

    # wierd cases:
    # Should a roi contain the empty roi?
    R((0, 0, 0), (10, 10, 10)).contains(R((None, None, None), (0, 0, 0)))

    # Should an empty roi contain the empty roi?
    R((None, None, None), (0, 0, 0)).contains(R((None, None, None), (0, 0, 0)))


def test_roi_operations_with_tuples():
    """
    We strictly check Coordinate type for many operations now
    """

    # No longer works (growing with tuples)
    R((0, 0, 0), (10, 10, 10)).grow((1, 2, 3), (1, 2, 3))

    # snap to grid with tuple voxel size
    R((0, 0, 0), (10, 10, 10)).snap_to_grid((4, 4, 4))
