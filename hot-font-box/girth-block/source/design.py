"""Girth Block: extremely wide, heavy rectilinear capitals and figures.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: BLOCK (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import BLOCK
from common import stroked, fit_all
from geometry import Polygon, scale
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Girth Block'
SLUG = 'girth-block'
STEM = 160
ADVANCE = 900
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

STRETCH = 1.3


def draw():
    shapes = {}
    for c, s in BLOCK.items():
        g = stroked(s, STEM, cap='flat', join='mitre', dot='square') if s else Polygon()
        shapes[c] = scale(g, xfact=STRETCH, yfact=1, origin=(0, 0)) if not g.is_empty else g
    return fit_all(shapes, sb=36, space=300, cell=ADVANCE)
