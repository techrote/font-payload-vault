"""Pillow Block: very heavy rectilinear letters with softened convex corners.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: BLOCK (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import BLOCK
from common import stroked, fit_all
from geometry import Polygon
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Pillow Block'
SLUG = 'pillow-block'
STEM = 150
ADVANCE = 700
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

R = 36


def draw():
    shapes = {}
    for c, s in BLOCK.items():
        g = stroked(s, STEM, cap='flat', join='mitre', dot='square') if s else Polygon()
        if not g.is_empty:
            g = g.buffer(-R, join_style='mitre').buffer(R, join_style='round')
        shapes[c] = g
    return fit_all(shapes, sb=38, space=240, cell=ADVANCE)
