"""Ingot Shadow: heavy condensed capitals with a stepped drop shadow.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: CONDENSED (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import CONDENSED
from common import stroked, fit_all
from geometry import Polygon, translate
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Ingot Shadow'
SLUG = 'ingot-shadow'
STEM = 100
ADVANCE = 480
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 520

STEPS = 7
STEP = (4, -4)
GAP = 12


def draw():
    shapes = {}
    for c, s in CONDENSED.items():
        g = stroked(s, STEM, cap='flat', join='bevel', dot='square') if s else Polygon()
        if not g.is_empty:
            shadow = unary_union([translate(g, STEP[0] * k, STEP[1] * k) for k in range(1, STEPS + 1)])
            g = g.union(shadow.difference(g.buffer(GAP)))
        shapes[c] = g
    return fit_all(shapes, sb=40, space=200, cell=ADVANCE)
