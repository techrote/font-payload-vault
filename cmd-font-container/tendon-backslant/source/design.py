"""Tendon Backslant: condensed sans leaning backwards (a back-slanted Regular, not a flagged style).
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: CONDENSED (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import CONDENSED
from common import stroked, fit_all
from geometry import Polygon, affine_transform
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Tendon Backslant'
SLUG = 'tendon-backslant'
STEM = 68
ADVANCE = 420
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 520

SLANT = -0.18


def draw():
    shapes = {}
    for c, s in CONDENSED.items():
        g = stroked(s, STEM, cap='flat', join='bevel', dot='square') if s else Polygon()
        shapes[c] = affine_transform(g, [1, SLANT, 0, 1, 0, 0]) if not g.is_empty else g
    return fit_all(shapes, sb=52, space=190, cell=ADVANCE)
