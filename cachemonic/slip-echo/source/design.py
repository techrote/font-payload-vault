"""Slip Echo: thin round strokes with an offset hollow echo.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: ROUND (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import ROUND
from common import stroked, fit_all
from geometry import translate, Polygon

FAMILY = 'Slip Echo'
SLUG = 'slip-echo'
STEM = 52
ADVANCE = 640
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

OFFSET = (36, -30)
GAP = 13


def draw():
    shapes = {}
    for c, s in ROUND.items():
        g = stroked(s, STEM, cap='round', join='round', dot='round') if s else Polygon()
        if not g.is_empty:
            echo = translate(g, *OFFSET).difference(g.buffer(GAP))
            g = g.union(echo)
        shapes[c] = g
    return fit_all(shapes, sb=60, space=260, cell=ADVANCE)
