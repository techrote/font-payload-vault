"""Bobbin Outline: heavy round letters drawn as a hollow outline.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: ROUND (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import ROUND
from common import stroked, fit_all
from geometry import Polygon
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Bobbin Outline'
SLUG = 'bobbin-outline'
STEM = 124
ADVANCE = 640
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

RIM = 20


def draw():
    shapes = {}
    for c, s in ROUND.items():
        outer = stroked(s, STEM, cap='round', join='round', dot='round') if s else Polygon()
        shapes[c] = outer.difference(outer.buffer(-RIM)) if not outer.is_empty else outer
    return fit_all(shapes, sb=50, space=260, cell=ADVANCE)
