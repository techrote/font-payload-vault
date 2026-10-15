"""Pebble Bold: bold, soft-ended round sans.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: ROUND (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import ROUND
from common import stroked, fit_all
from geometry import Polygon
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Pebble Bold'
SLUG = 'pebble-bold'
STEM = 118
ADVANCE = 640
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500


def draw():
    shapes = {c: stroked(s, STEM, cap='round', join='round', dot='round') if s else Polygon()
              for c, s in ROUND.items()}
    return fit_all(shapes, sb=50, space=250, cell=ADVANCE)
