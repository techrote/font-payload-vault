"""Skiff Slant: slanted monoline round-capped sans (a slanted Regular, not a flagged italic).
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: ROUND (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import ROUND
from common import stroked, fit_all
from geometry import Polygon, affine_transform
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Skiff Slant'
SLUG = 'skiff-slant'
STEM = 66
ADVANCE = 600
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

SLANT = 0.2


def draw():
    shapes = {}
    for c, s in ROUND.items():
        g = stroked(s, STEM, cap='round', join='round', dot='round') if s else Polygon()
        if not g.is_empty:
            g = affine_transform(g, [1, SLANT, 0, 1, 0, 0])
        shapes[c] = g
    return fit_all(shapes, sb=70, space=250, cell=ADVANCE)
