from typing import Iterable

from .coordinate import Coordinate


class FloatCoordinate(Coordinate):
    """A ``tuple`` of numbers or None.

    Like :class:`Coordinate`, but preserves float values instead of casting to
    int. Supports all the same element-wise arithmetic operations.

    FloatCoordinates can be initialized with any iterable of numbers, e.g.::

        FloatCoordinate(1.0, 2.0, 3.0)
        FloatCoordinate([1, 2, 3])

    FloatCoordinates can also pack multiple args into an iterable, e.g.::

        FloatCoordinate(1, 2, 3)
    """

    def __new__(cls, *array_like):
        if len(array_like) == 1 and isinstance(array_like[0], Iterable):
            array_like = array_like[0]
        return tuple.__new__(cls, [x if x is not None else None for x in array_like])
