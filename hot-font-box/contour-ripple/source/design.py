"""Contour Ripple: heavy round letters with two concentric engraved contour lines.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: ROUND (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import ROUND
from common import stroked, fit_all
from geometry import Polygon
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Contour Ripple'
SLUG = 'contour-ripple'
STEM = 150
ADVANCE = 660
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

DEPTHS = (22, 46)
GROOVE = 12


def draw():
    shapes = {}
    for c, s in ROUND.items():
        g = stroked(s, STEM, cap='round', join='round', dot='round') if s else Polygon()
        if not g.is_empty:
            grooves = [g.buffer(-d).difference(g.buffer(-d - GROOVE)) for d in DEPTHS]
            g = g.difference(unary_union(grooves))
        shapes[c] = g
    return fit_all(shapes, sb=48, space=260, cell=ADVANCE)
