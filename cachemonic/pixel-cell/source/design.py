"""Pixel Cell: slab serif resampled onto a 50-unit pixel grid.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: SLAB (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import SLAB
from common import stroked, fit_all
from geometry import Polygon, box
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Pixel Cell'
SLUG = 'pixel-cell'
STEM = 110
ADVANCE = 720
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

P = 50
COVER = 0.45


def pixelate(g):
    x0, y0, x1, y1 = g.bounds
    cells = []
    for gx in range(int(x0 // P) * P, int(x1) + P, P):
        for gy in range(int(y0 // P) * P, int(y1) + P, P):
            cell = box(gx, gy, gx + P, gy + P)
            if g.intersection(cell).area >= COVER * P * P:
                cells.append(cell)
    return unary_union(cells) if cells else Polygon()


def draw():
    shapes = {}
    for c, s in SLAB.items():
        g = stroked(s, STEM, cap='flat', join='mitre', dot='square') if s else Polygon()
        shapes[c] = pixelate(g) if not g.is_empty else g
    return fit_all(shapes, sb=50, space=260, cell=ADVANCE)
