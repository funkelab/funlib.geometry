from .coordinate import Coordinate
from .float_coordinate import FloatCoordinate
from .roi import Roi


class FloatRoi(Roi):
    """A rectangular region of interest with float-valued coordinates.

    Like :class:`Roi`, but uses :class:`FloatCoordinate` instead of
    :class:`Coordinate`, preserving float precision in offsets and shapes.
    """

    _coord_type = FloatCoordinate

    @property
    def center(self) -> "Coordinate":
        """Get the center of this ROI using floor division."""
        return self.offset + self.shape // 2
