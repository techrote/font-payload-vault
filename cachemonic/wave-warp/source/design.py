"""Wave Warp: thin round letters bent sideways by a sine wave along their height.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: ROUND (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import ROUND
from common import stroked, fit_all
from geometry import Polygon
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Wave Warp'
SLUG = 'wave-warp'
STEM = 70
ADVANCE = 660
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

import numpy as np
import shapely

AMP = 26
PERIOD = 420


def warp(g):
    g = shapely.segmentize(g, 18)
    g = shapely.transform(g, lambda a: np.column_stack(
        (a[:, 0] + AMP * np.sin(a[:, 1] / PERIOD * 2 * np.pi), a[:, 1])))
    return g if g.is_valid else g.buffer(0)


def draw():
    shapes = {}
    for c, s in ROUND.items():
        g = stroked(s, STEM, cap='round', join='round', dot='round') if s else Polygon()
        shapes[c] = warp(g) if not g.is_empty else g
    return fit_all(shapes, sb=70, space=250, cell=ADVANCE)
