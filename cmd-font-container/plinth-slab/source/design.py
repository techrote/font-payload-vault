"""Plinth Slab: regular-weight slab serif with flat mitred strokes.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: SLAB (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import SLAB
from common import stroked, fit_all
from geometry import Polygon
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Plinth Slab'
SLUG = 'plinth-slab'
STEM = 64
ADVANCE = 660
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500


def draw():
    shapes = {c: stroked(s, STEM, cap='flat', join='mitre', dot='square') if s else Polygon()
              for c, s in SLAB.items()}
    return fit_all(shapes, sb=52, space=250, cell=ADVANCE)
