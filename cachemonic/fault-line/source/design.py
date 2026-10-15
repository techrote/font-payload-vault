"""Fault Line: condensed strokes sheared along a diagonal fault.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: CONDENSED (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import CONDENSED
from common import stroked, fit_all
from geometry import translate, Polygon, LineString

FAMILY = 'Fault Line'
SLUG = 'fault-line'
STEM = 74
ADVANCE = 400
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 520

SLOPE = 0.5
BASE = 230
SHIFT = 38
GAP = 8
UPPER = Polygon([(-1500, SLOPE * -1500 + BASE), (1500, SLOPE * 1500 + BASE), (1500, 3000), (-1500, 3000)])
SEAM = LineString([(-1500, SLOPE * -1500 + BASE), (1500, SLOPE * 1500 + BASE)]).buffer(GAP)


def draw():
    shapes = {}
    for c, s in CONDENSED.items():
        g = stroked(s, STEM, cap='flat', join='bevel', dot='square') if s else Polygon()
        if not g.is_empty:
            top = g.intersection(UPPER)
            low = g.difference(UPPER)
            g = translate(top, SHIFT, 0).union(low).difference(SEAM)
        shapes[c] = g
    return fit_all(shapes, sb=44, space=190, cell=ADVANCE)
