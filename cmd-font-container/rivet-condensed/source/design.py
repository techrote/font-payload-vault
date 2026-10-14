"""Rivet Condensed: bold flat-ended condensed sans for narrow columns.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: CONDENSED (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import CONDENSED
from common import stroked, fit_all
from geometry import Polygon

FAMILY = 'Rivet Condensed'
SLUG = 'rivet-condensed'
STEM = 100
ADVANCE = 400
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 520


def draw():
    shapes = {c: stroked(s, STEM, cap='flat', join='bevel', dot='square') if s else Polygon()
              for c, s in CONDENSED.items()}
    return fit_all(shapes, sb=44, space=190, cell=ADVANCE)
