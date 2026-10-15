"""Stride Wide: extended monoline round sans, stretched horizontally.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: ROUND (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import ROUND
from common import stroked, fit_all
from geometry import Polygon, scale
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Stride Wide'
SLUG = 'stride-wide'
STEM = 60
ADVANCE = 760
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

STRETCH = 1.35


def draw():
    shapes = {}
    for c, s in ROUND.items():
        g = stroked(s, STEM, cap='round', join='round', dot='round') if s else Polygon()
        shapes[c] = scale(g, xfact=STRETCH, yfact=1, origin=(0, 0)) if not g.is_empty else g
    return fit_all(shapes, sb=80, space=300, cell=ADVANCE)
