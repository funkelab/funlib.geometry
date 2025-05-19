from funlib.geometry import Array, Roi, Coordinate
import numpy as np
import pytest

def test_constructor():
    offset = Coordinate(1, -1, 2.5)
    shape = Coordinate(10, 10, 10)
    voxel_size = Coordinate(1, 1, 1)

    arr = Array(Roi(offset=offset, shape=shape), voxel_size=voxel_size)
    assert arr.roi.offset == offset
    assert arr.roi.shape == shape
    assert arr.voxel_size == voxel_size
    assert arr.shape == shape

    voxel_size = Coordinate(2, 2, 2)
    arr = Array(Roi(offset=offset, shape=shape), voxel_size=voxel_size)
    assert arr.shape == Coordinate(5, 5, 5)

    voxel_size = Coordinate(2, 2, 3)
    with pytest.raises(ValueError, match="Roi shape .* is not evenly divisible by voxel size"):
        arr = Array(Roi(offset=offset, shape=shape), voxel_size=voxel_size)


def test_to_pixel_world_space_coordinate():
    offset = Coordinate(1, -1, 2.5)
    shape = Coordinate(10, 10, 10)
    voxel_size = Coordinate(1, 1, 1)

    arr = Array(Roi(offset=offset, shape=shape), voxel_size=voxel_size)
    world_loc = Coordinate(1, -1, 2.5)
    pixel_loc = Coordinate(0, 0, 0)
    assert arr.to_pixel_space(world_loc) == pixel_loc
    assert arr.to_world_space(pixel_loc) == world_loc

    offset = Coordinate(1, 1.5, 2.5)
    shape = Coordinate(9, 9, 10)
    voxel_size = Coordinate(1.5, 1.5, 1)

    arr = Array(Roi(offset=offset, shape=shape), voxel_size=voxel_size)
    pixel_loc = Coordinate(1.0, 1.0, 1.0)
    world_loc = Coordinate(2.5, 3.0, 3.5)
    assert arr.to_world_space(pixel_loc) == world_loc
    assert arr.to_pixel_space(world_loc) == pixel_loc

def test_to_pixel_world_space_roi():
    offset = Coordinate(1, -1, 2.5)
    shape = Coordinate(10, 10, 10)
    voxel_size = Coordinate(1, 1, 1)
    arr = Array(Roi(offset=offset, shape=shape), voxel_size=voxel_size)

    world_loc = Roi((1, -1, 2.5), (10, 10, 10))
    pixel_loc = Roi((0, 0, 0,), (10, 10, 10))
    assert arr.to_pixel_space(world_loc) == pixel_loc
    assert arr.to_world_space(pixel_loc) == world_loc

    offset = Coordinate(1, 1.5, 2.5)
    shape = Coordinate(9, 9, 10)
    voxel_size = Coordinate(1.5, 1.5, 1)
    arr = Array(Roi(offset=offset, shape=shape), voxel_size=voxel_size)

    pixel_loc = Roi((1.0, 1.0, 1.0), (1.0, 1.0, 1.0))
    world_loc = Roi((2.5, 3.0, 3.5), (1.5, 1.5, 1.0))
    assert arr.to_world_space(pixel_loc) == world_loc
    assert arr.to_pixel_space(world_loc) == pixel_loc

def test_to_slices_coordinate():
    offset = Coordinate((0,))
    shape = Coordinate((10,))
    voxel_size = Coordinate((2.5,))
    data = np.array([1, 2, 3, 4])
    arr = Array(Roi(offset=offset, shape=shape), voxel_size=voxel_size)

    world_loc = Coordinate((0,))
    print(arr.to_slices(world_loc))
    assert data[arr.to_slices(world_loc)] == 1
    world_loc = Coordinate((1.2,))
    assert data[arr.to_slices(world_loc)] == 1
    world_loc = Coordinate((2.5,))
    assert data[arr.to_slices(world_loc)] == 2

    world_loc = Coordinate((5.0,))
    assert data[arr.to_slices(world_loc)] == 3

    world_loc = Coordinate((7.5,))
    assert data[arr.to_slices(world_loc)] == 4

    world_loc = Coordinate((9.9,))
    assert data[arr.to_slices(world_loc)] == 4

    world_loc = Coordinate((10.0,))
    with pytest.raises(ValueError, match="Given world location"):
        arr.to_slices(world_loc)

def test_to_slices_roi():
    offset = Coordinate((0,))
    shape = Coordinate((10,))
    voxel_size = Coordinate((2.5,))
    data = np.array([1, 2, 3, 4])
    arr = Array(Roi(offset=offset, shape=shape), voxel_size=voxel_size)

    world_roi = Roi(offset=(2.5,), shape=(5,))
    np.testing.assert_array_equal(data[arr.to_slices(world_roi)], np.array([2, 3]))
    # world_roi = Roi(offset=(0,), shape=(None,))
    # assert data[arr.to_slices(world_roi)] == data

    world_roi = Roi(offset=(2.5,), shape=(4,))
    with pytest.raises(ValueError, match="Pixel roi .* cannot be converted to slices"):
        arr.to_slices(world_roi)

    world_roi = Roi(offset=(2.0,), shape=(5,))
    with pytest.raises(ValueError, match="Pixel roi .* cannot be converted to slices"):
        arr.to_slices(world_roi)