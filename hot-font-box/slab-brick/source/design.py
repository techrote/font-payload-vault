"""Slab Brick: very heavy rectilinear capitals and figures.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: BLOCK (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import BLOCK
from common import stroked, fit_all
from geometry import Polygon
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Slab Brick'
SLUG = 'slab-brick'
STEM = 142
ADVANCE = 700
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500


def draw():
    shapes = {c: stroked(s, STEM, cap='flat', join='mitre', dot='square') if s else Polygon()
              for c, s in BLOCK.items()}
    return fit_all(shapes, sb=36, space=240, cell=ADVANCE)
