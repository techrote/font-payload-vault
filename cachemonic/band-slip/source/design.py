"""Band Slip: condensed strokes whose horizontal bands slip sideways in a fixed cycle.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: CONDENSED (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import CONDENSED
from common import stroked, fit_all
from geometry import Polygon, box, translate
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Band Slip'
SLUG = 'band-slip'
STEM = 80
ADVANCE = 440
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 520

BAND = 90
SHIFTS = (0, 24, -14, 32, -8, 18)


def draw():
    shapes = {}
    for c, s in CONDENSED.items():
        g = stroked(s, STEM, cap='flat', join='bevel', dot='square') if s else Polygon()
        if not g.is_empty:
            parts = []
            for i, y in enumerate(range(-360, 900, BAND)):
                part = g.intersection(box(-300, y, 1200, y + BAND))
                if not part.is_empty:
                    parts.append(translate(part, SHIFTS[i % len(SHIFTS)], 0))
            g = unary_union(parts)
        shapes[c] = g
    return fit_all(shapes, sb=46, space=200, cell=ADVANCE)
