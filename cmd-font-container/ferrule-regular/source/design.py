"""Ferrule Regular: medium-weight round sans with flat, cut-off stroke ends.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: ROUND (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import ROUND
from common import stroked, fit_all
from geometry import Polygon
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Ferrule Regular'
SLUG = 'ferrule-regular'
STEM = 86
ADVANCE = 620
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500


def draw():
    shapes = {c: stroked(s, STEM, cap='flat', join='round', dot='square') if s else Polygon()
              for c, s in ROUND.items()}
    return fit_all(shapes, sb=58, space=250, cell=ADVANCE)
