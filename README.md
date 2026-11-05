[![tests](https://github.com/funkelab/funlib.geometry/actions/workflows/tests.yaml/badge.svg)](https://github.com/funkelab/funlib.geometry/actions/workflows/tests.yaml)
[![lint](https://github.com/funkelab/funlib.geometry/actions/workflows/lint.yaml/badge.svg)](https://github.com/funkelab/funlib.geometry/actions/workflows/lint.yaml)
[![publish](https://github.com/funkelab/funlib.geometry/actions/workflows/publish.yaml/badge.svg)](https://pypi.org/project/funlib.geometry/)

# funlib.geometry
A package for Coordinates, Rois and common operations in Coordinate spaces

## Install

```bash
pip install funlib.geometry    # or: uv add funlib.geometry
```

## Usage

### Coordinate

An immutable tuple of integers with element-wise arithmetic:

```python
from funlib.geometry import Coordinate

a = Coordinate(1, 2, 3)
b = Coordinate(4, 5, 6)

a + b        # Coordinate(5, 7, 9)
a * 2        # Coordinate(2, 4, 6)
a * b        # Coordinate(4, 10, 18)
abs(-a)      # Coordinate(1, 2, 3)
```

Use `None` for unbounded dimensions:

```python
Coordinate(1, None, 3) + Coordinate(4, 5, 6)  # Coordinate(5, None, 9)
```

### Roi

A rectangular region defined by an offset and shape:

```python
from funlib.geometry import Roi, Coordinate

roi = Roi((0, 0, 0), (10, 20, 30))

roi.offset   # Coordinate(0, 0, 0)
roi.shape    # Coordinate(10, 20, 30)
roi.begin    # Coordinate(0, 0, 0)
roi.end      # Coordinate(10, 20, 30)
roi.center   # Coordinate(5, 10, 15)
roi.size     # 6000
```

Arithmetic shifts the offset (`+`/`-`) or scales both offset and shape (`*`/`/`/`//`):

```python
roi + Coordinate(1, 2, 3)  # Roi((1, 2, 3), (10, 20, 30))
roi * 2                     # Roi((0, 0, 0), (20, 40, 60))
```

Intersection, union, and containment:

```python
a = Roi((0, 0), (10, 10))
b = Roi((5, 5), (10, 10))

a.intersect(b)   # Roi((5, 5), (5, 5))
a.union(b)       # Roi((0, 0), (15, 15))
a.contains(b)    # False
a.contains((3, 3))  # True
```

Snap to a grid and convert to numpy slices:

```python
import numpy as np

roi = Roi((3, 7), (10, 10))
roi.snap_to_grid(Coordinate(4, 4), mode="grow")  # Roi((0, 4), (16, 16))

data = np.zeros((100, 100))
region = data[roi.to_slices()]  # equivalent to data[3:13, 7:17]
```

## Contributing

The commands below are the ones CI runs, so a green local run means a green PR.

```bash
git clone https://github.com/funkelab/funlib.geometry
cd funlib.geometry
uv sync                                             # Python, dependencies, dev tools (from uv.lock)
uv run pytest                                       # tests with coverage
uv run pytest --no-cov tests/<file>.py              # one file, without the coverage floor
uv run ruff check . && uv run ruff format --check . # lint and formatting
uv run ty check                                     # types
```

`uv.lock` pins the development environment; the `lock-upgrade` workflow refreshes it monthly and opens a pull request.
