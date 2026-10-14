"""Saw Warp: slab serif bent sideways by a triangle wave, giving zigzag stems.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: SLAB (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import SLAB
from common import stroked, fit_all
from geometry import Polygon
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Saw Warp'
SLUG = 'saw-warp'
STEM = 92
ADVANCE = 720
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

import numpy as np
import shapely

AMP = 30
PERIOD = 300


def tri(y):
    return (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * y / PERIOD))


def warp(g):
    g = shapely.segmentize(g, 15)
    g = shapely.transform(g, lambda a: np.column_stack((a[:, 0] + AMP * tri(a[:, 1]), a[:, 1])))
    return g if g.is_valid else g.buffer(0)


def draw():
    shapes = {}
    for c, s in SLAB.items():
        g = stroked(s, STEM, cap='flat', join='mitre', dot='square') if s else Polygon()
        shapes[c] = warp(g) if not g.is_empty else g
    return fit_all(shapes, sb=50, space=260, cell=ADVANCE)
