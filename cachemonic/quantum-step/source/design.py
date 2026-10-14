"""Quantum Step: round skeleton snapped to a 60-unit grid so curves become stair-steps.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: ROUND (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import ROUND
from common import stroked, fit_all
from geometry import Polygon, set_precision
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Quantum Step'
SLUG = 'quantum-step'
STEM = 92
ADVANCE = 620
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

GRID = 60


def draw():
    shapes = {}
    for c, s in ROUND.items():
        g = stroked(s, STEM, cap='round', join='round', dot='round') if s else Polygon()
        if not g.is_empty:
            g = set_precision(g, GRID)
            if not g.is_valid:
                g = g.buffer(0)
        shapes[c] = g
    return fit_all(shapes, sb=56, space=260, cell=ADVANCE)
