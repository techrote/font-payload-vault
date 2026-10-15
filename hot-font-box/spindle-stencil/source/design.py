"""Spindle Stencil: heavy rounded stencil capitals with cut bridges.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: ROUND (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import ROUND
from common import stroked, fit_all
from geometry import box, Polygon

FAMILY = 'Spindle Stencil'
SLUG = 'spindle-stencil'
STEM = 132
ADVANCE = 620
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

# Bridge cuts: (glyph set, y of the cut). Glyphs with crossbars are left whole.
CAPS_CUT = 'CDGJOQSU0689'
LOWER_CUT = 'bcdgopqsu'
CUT = 34


def draw():
    shapes = {}
    for c, s in ROUND.items():
        g = stroked(s, STEM, cap='flat', join='round', dot='square') if s else Polygon()
        if c in CAPS_CUT:
            g = g.difference(box(-100, 350 - CUT / 2, 900, 350 + CUT / 2))
        elif c in LOWER_CUT:
            g = g.difference(box(-100, 250 - CUT / 2, 900, 250 + CUT / 2))
        shapes[c] = g
    return fit_all(shapes, sb=55, space=260, cell=ADVANCE)
