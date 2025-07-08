from .roi import Roi
from .coordinate import Coordinate

class Array:
    """A set of voxels that discretize a roi at a given voxel size
    """
    @classmethod
    def from_world(cls, world_offset: Coordinate, world_shape: Coordinate, voxel_size: Coordinate):
        world_roi = Roi(world_offset, world_shape)
        return cls(world_roi, voxel_size)
    
    @classmethod
    def from_pixels(cls, pixel_shape: Coordinate, voxel_size: Coordinate, world_offset: Coordinate | None = None, pixel_offset: Coordinate | None = None):
        if world_offset is None and pixel_offset is not None:
            world_offset = Coordinate(pixel_offset) * voxel_size
        
        if world_offset is None:
            world_offset = Coordinate([0,]*len(voxel_size))

        world_shape = Coordinate(pixel_shape) * Coordinate(voxel_size)
        
        world_roi = Roi(world_offset, world_shape)
        return cls(world_roi, voxel_size)


    def __init__(self, world_roi: Roi, voxel_size: Coordinate):
        self.roi = world_roi
        self.voxel_size = voxel_size
        self.shape = self.roi.shape / self.voxel_size
        for d in range(self.roi.dims):
            if int(self.shape[d]) != self.shape[d]:
                raise ValueError(f"Roi shape {self.roi.shape} is not evenly divisible by voxel size {self.voxel_size}")

    def to_pixel_space(self, world_loc: Roi | Coordinate) -> Roi | Coordinate:
        if not self.roi.contains(world_loc):
            raise ValueError(f"Given world location {world_loc} is not included in this array with world ROI {self.roi}")
        return (world_loc - self.roi.offset) / self.voxel_size
    
    def to_world_space(self, pixel_loc: Roi | Coordinate) -> Roi | Coordinate:
        return pixel_loc * self.voxel_size + self.roi.offset
    
    def to_slices(self, world_loc: Roi | Coordinate) -> tuple[slice, ...]:
        """Get a ``tuple`` of ``slice`` that represent this ROI/coordinate and can be used
        to index the array."""
        pixel_loc = self.to_pixel_space(world_loc)
        slices = []
        if isinstance(pixel_loc, Coordinate):
            # round down to get the pixel containing the location
            for d in range(pixel_loc.dims):
                if pixel_loc[d] is None:
                    s = None
                else:
                    s = int(pixel_loc[d])
                slices.append(s)
        elif isinstance(pixel_loc, Roi):
            for d in range(pixel_loc.dims):
                offset = pixel_loc.offset[d]
                int_offset = int(offset)
                if int_offset != offset:
                    raise ValueError(f"Pixel roi {pixel_loc} cannot be converted to slices")
                shape = pixel_loc.shape[d]
                if shape is None:
                    s = slice(None, None)
                elif shape == 0:
                    s = slice(None, 0)
                else:
                    int_shape = int(shape)
                    if int_shape != shape:
                        raise ValueError(f"Pixel roi {pixel_loc} cannot be converted to slices")
                    s = slice(int_offset, int_offset + int_shape)
                slices.append(s)
        
        return tuple(slices)
