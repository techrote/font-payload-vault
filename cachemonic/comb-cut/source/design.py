"""Comb Cut: heavy condensed strokes cut by fine vertical comb slits.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: CONDENSED (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import CONDENSED
from common import stroked, fit_all
from geometry import Polygon, box
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Comb Cut'
SLUG = 'comb-cut'
STEM = 96
ADVANCE = 440
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 520

PITCH = 58
SLIT = 13
COMB = unary_union([box(x, -400, x + SLIT, 1000) for x in range(-300, 900, PITCH)])


def draw():
    shapes = {}
    for c, s in CONDENSED.items():
        g = stroked(s, STEM, cap='flat', join='bevel', dot='square') if s else Polygon()
        shapes[c] = g.difference(COMB) if not g.is_empty else g
    return fit_all(shapes, sb=44, space=200, cell=ADVANCE)
