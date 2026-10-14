"""Hatch Block: heavy rectilinear letters engraved with diagonal hatch cuts.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: BLOCK (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import BLOCK
from common import stroked, fit_all
from geometry import Polygon, LineString
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Hatch Block'
SLUG = 'hatch-block'
STEM = 130
ADVANCE = 680
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

PITCH = 46
CUT = 11
HATCH = unary_union([LineString([(k, -340), (k + 1300, 960)]).buffer(CUT / 2) for k in range(-1400, 1000, PITCH)])


def draw():
    shapes = {}
    for c, s in BLOCK.items():
        g = stroked(s, STEM, cap='flat', join='mitre', dot='square') if s else Polygon()
        shapes[c] = g.difference(HATCH) if not g.is_empty else g
    return fit_all(shapes, sb=40, space=240, cell=ADVANCE)
