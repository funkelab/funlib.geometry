import warnings

from .coordinate import Coordinate as _Coordinate  # noqa
from .float_coordinate import FloatCoordinate  # noqa
from .float_roi import FloatRoi  # noqa
from .roi import Roi  # noqa

__all__ = ["Coordinate", "FloatCoordinate", "Roi", "FloatRoi"]

__major__ = 0
__minor__ = 3
__patch__ = 0
__tag__ = ""
__version__ = "{}.{}.{}{}".format(__major__, __minor__, __patch__, __tag__).strip(".")


def __getattr__(name):
    if name == "Coordinate":
        warnings.warn(
            "Coordinate is deprecated, use FloatCoordinate instead. "
            "Coordinate will be removed in a future version.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _Coordinate
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
