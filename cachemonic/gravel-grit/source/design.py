"""Gravel Grit: heavy round letters pitted by deterministic grit holes.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: ROUND (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import ROUND
from common import stroked, fit_all
from geometry import Polygon, disc
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Gravel Grit'
SLUG = 'gravel-grit'
STEM = 130
ADVANCE = 660
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

import random

HOLES = 34
RMIN, RMAX = 7, 19


def pit(c, g):
    rng = random.Random(ord(c))
    x0, y0, x1, y1 = g.bounds
    holes = [disc(rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(RMIN, RMAX)) for _ in range(HOLES)]
    return g.difference(unary_union(holes))


def draw():
    shapes = {}
    for c, s in ROUND.items():
        g = stroked(s, STEM, cap='round', join='round', dot='round') if s else Polygon()
        shapes[c] = pit(c, g) if not g.is_empty else g
    return fit_all(shapes, sb=50, space=260, cell=ADVANCE)
