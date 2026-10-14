"""Tallow Condensed: medium condensed sans with soft round ends and joins.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: CONDENSED (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import CONDENSED
from common import stroked, fit_all
from geometry import Polygon
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Tallow Condensed'
SLUG = 'tallow-condensed'
STEM = 72
ADVANCE = 420
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 520


def draw():
    shapes = {c: stroked(s, STEM, cap='round', join='round', dot='round') if s else Polygon()
              for c, s in CONDENSED.items()}
    return fit_all(shapes, sb=50, space=190, cell=ADVANCE)
