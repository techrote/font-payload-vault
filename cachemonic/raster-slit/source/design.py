"""Raster Slit: medium round strokes cut by horizontal scan slits.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: ROUND (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import ROUND
from common import stroked, fit_all
from geometry import Polygon, box
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Raster Slit'
SLUG = 'raster-slit'
STEM = 96
ADVANCE = 640
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

PITCH = 44
SLIT = 12
SLITS = unary_union([box(-200, y, 1200, y + SLIT) for y in range(-320, 900, PITCH)])


def draw():
    shapes = {}
    for c, s in ROUND.items():
        g = stroked(s, STEM, cap='round', join='round', dot='round') if s else Polygon()
        shapes[c] = g.difference(SLITS) if not g.is_empty else g
    return fit_all(shapes, sb=56, space=260, cell=ADVANCE)
