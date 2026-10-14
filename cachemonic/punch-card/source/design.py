"""Punch Card: heavy rectilinear letters perforated by a round-hole lattice.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: BLOCK (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import BLOCK
from common import stroked, fit_all
from geometry import Polygon, disc
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Punch Card'
SLUG = 'punch-card'
STEM = 150
ADVANCE = 700
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

PITCH = 54
HOLE = 12
HOLES = unary_union([disc(x, y, HOLE) for x in range(-200, 1000, PITCH) for y in range(-330, 900, PITCH)])


def draw():
    shapes = {}
    for c, s in BLOCK.items():
        g = stroked(s, STEM, cap='flat', join='mitre', dot='square') if s else Polygon()
        shapes[c] = g.difference(HOLES) if not g.is_empty else g
    return fit_all(shapes, sb=40, space=240, cell=ADVANCE)
