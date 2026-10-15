"""Misprint Duo: two overprinted condensed outlines, slightly out of register.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: CONDENSED (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import CONDENSED
from common import stroked, fit_all
from geometry import Polygon, translate
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Misprint Duo'
SLUG = 'misprint-duo'
STEM = 84
ADVANCE = 470
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 520

RIM = 11
OFFSET = (22, -14)


def outline(g):
    return g.difference(g.buffer(-RIM))


def draw():
    shapes = {}
    for c, s in CONDENSED.items():
        g = stroked(s, STEM, cap='flat', join='bevel', dot='square') if s else Polygon()
        shapes[c] = outline(g).union(outline(translate(g, *OFFSET))) if not g.is_empty else g
    return fit_all(shapes, sb=44, space=210, cell=ADVANCE)
