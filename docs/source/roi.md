# Coordinates and ROIs

`Coordinate` and `Roi` are the two types every package in this family passes
around: a point or size in an N-dimensional integer space, and a rectangular
region of that space. This page states their rules; the [API](api) page
lists every method.

## Coordinate

A `Coordinate` is an immutable tuple of integers. Arithmetic is element-wise
and accepts another `Coordinate` or a single number:

```python
from funlib.geometry import Coordinate

shape = Coordinate(2, 3, 4)
voxel_size = Coordinate(10, 5, 1)
shape * voxel_size      # Coordinate(20, 15, 4)
shape * 2 + 1           # Coordinate(5, 7, 9)
-shape, abs(-shape)     # Coordinate(-2, -3, -4), Coordinate(2, 3, 4)
```

Division always yields integers. `/` truncates toward zero and `//` floors,
so they only differ for negative values:

```python
Coordinate(7, 8) / 2       # Coordinate(3, 4)
Coordinate(-7, 8) / 2      # Coordinate(-3, 4)
Coordinate(-7, 8) // 2     # Coordinate(-4, 4)
```

`round_division`, `floor_division` and `ceil_division` round to the nearest,
previous or next multiple, and `is_multiple_of` tests divisibility. These are
what `Roi.snap_to_grid` uses.

An entry may be `None`, meaning "unbounded" along that axis. `None` absorbs
every operation:

```python
Coordinate(None, 1, 2) + Coordinate(3, 4, None)   # Coordinate(None, 5, None)
```

A `Coordinate` compares equal to a plain tuple with the same entries, so it
can stand in wherever a tuple is expected, and `dims` is its length.

## Roi

A `Roi` is an offset plus a shape. Its interval is half-open on every axis:
`begin` (the offset) is inside, `end` (`offset + shape`) is not.

```python
from funlib.geometry import Roi

roi = Roi((3, 7), (10, 10))
roi.begin, roi.end     # Coordinate(3, 7), Coordinate(13, 17)
roi.contains((12, 16)) # True
roi.contains((13, 16)) # False: end is exclusive
roi.to_slices()        # (slice(3, 13), slice(7, 17)), for numpy indexing
roi.center, roi.size   # Coordinate(8, 12), 100
```

A `Roi` contains another `Roi` when it contains its `begin` and its last
voxel, `end - 1`. A `Roi` is never guessed to a different number of
dimensions: offset and shape must have the same length, and a `Roi` without
an offset is not a thing (use a `Coordinate` for a bare shape).

### Unbounded and empty ROIs

A `None` in the shape makes that axis unbounded; the offset on that axis is
then `None` too, and so is the end. `size` is `None`, `unbounded` is `True`,
and `to_slices` gives `slice(None)` on that axis. Unbounded ROIs contain
everything along the open axes, and intersecting with one clips the other
ROI:

```python
everything = Roi((None, 0), (None, 10))
everything.contains((-1000, 5))                 # True
everything.intersect(Roi((5, 5), (10, 10)))     # Roi((5, 5), (10, 5))
```

An empty ROI has a shape of zeros and an offset of `None`; its `empty` is
`True` and it prints as `[empty ROI]`. It is what `intersect` returns when
two ROIs do not overlap, so check `empty` rather than `size == 0` when the
ROI may be unbounded.

Setting `shape` to `None` turns an existing ROI unbounded; setting it to a
tuple of ints while the offset is still `None` leaves a shape without a
position, and setting the offset afterwards makes it a regular ROI again.

### Arithmetic

Adding or subtracting a `Coordinate` or an int shifts the offset and keeps
the shape (`shift` is the same operation). Multiplying or dividing scales
both offset and shape, which is how a ROI in voxels becomes a ROI in world
units and back:

```python
voxel_size = Coordinate(2, 3)
roi * voxel_size            # Roi((6, 21), (20, 30))
Roi((2, 4), (10, 9)) / 2    # Roi((1, 2), (5, 4)): integer division
roi + 1                     # Roi((4, 8), (10, 10))
```

### Growing and shrinking

`grow(amount_neg, amount_pos)` extends the ROI by `amount_neg` toward the
origin and by `amount_pos` away from it. Each amount is a `Coordinate` or a
single int applied to every axis. Negative amounts shrink the ROI:

```python
roi.grow(1, 1)        # Roi((2, 6), (12, 12))
roi.grow(-1, -1)      # Roi((4, 8), (8, 8))
roi.grow(2, -2)       # Roi((1, 5), (10, 10)): moved, same shape
```

Nothing stops a shrink from producing a negative shape; check `empty` or
`shape` afterwards if the amounts come from data.

### Intersection and union

`intersect` returns the overlap, or an empty ROI when there is none.
`intersects` answers the question without building the result. `union`
returns the smallest ROI containing both, including the gap between them:

```python
a, b = Roi((0, 0), (5, 5)), Roi((10, 10), (5, 5))
a.intersect(b)   # [empty ROI]
a.union(b)       # Roi((0, 0), (15, 15))
```

### Snapping to a grid

`snap_to_grid(voxel_size, mode)` aligns `begin` and `end` to multiples of
`voxel_size`, so the result can be read from or written to a dataset with
that voxel size without partial voxels. The three modes differ in how they
round:

| mode | `begin` | `end` | `Roi((1,), (7,))` on a grid of 2 | on a grid of 3 |
|------|---------|-------|---------------------------------|----------------|
| `"grow"` (default) | down | up | `Roi((0,), (8,))` | `Roi((0,), (9,))` |
| `"shrink"` | up | down | `Roi((2,), (6,))` | `Roi((3,), (3,))` |
| `"closest"` | nearest | nearest | `Roi((0,), (8,))` | `Roi((0,), (9,))` |

`"grow"` is the mode for reading: it never loses data. `"shrink"` is the
mode for writing: it never touches voxels outside the ROI. `"closest"` can
return an empty ROI when the region is smaller than a voxel, for example
`Roi((3,), (2,))` on a grid of 4. Unbounded axes stay unbounded in every
mode; the voxel size must have the same number of dimensions as the ROI and
no zeros.
