"""Cantilever Shadow: heavy condensed capitals with a thin wireframe shadow offset behind.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: CONDENSED (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import CONDENSED
from common import stroked, fit_all
from geometry import Polygon, translate
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Cantilever Shadow'
SLUG = 'cantilever-shadow'
STEM = 110
ADVANCE = 560
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 520

OFFSET = (42, -42)
LINE = 26
GAP = 10


def draw():
    shapes = {}
    for c, s in CONDENSED.items():
        if not s:
            shapes[c] = Polygon()
            continue
        g = stroked(s, STEM, cap='flat', join='bevel', dot='square')
        wire = translate(stroked(s, LINE, cap='flat', join='bevel', dot='square'), *OFFSET)
        shapes[c] = g.union(wire.difference(g.buffer(GAP)))
    return fit_all(shapes, sb=40, space=220, cell=ADVANCE)
