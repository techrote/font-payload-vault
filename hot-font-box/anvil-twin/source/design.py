"""Anvil Twin: heavy slab serif with a wide groove that splits each stroke into twin rails.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: SLAB (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import SLAB
from common import stroked, fit_all
from geometry import Polygon, path
from shapely.ops import unary_union  # noqa: F401

FAMILY = 'Anvil Twin'
SLUG = 'anvil-twin'
STEM = 150
ADVANCE = 780
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 500

GROOVE = 70
RIM = 26


def _is_dot(sub):
    t = sub.split()
    return len(t) == 6 and t[3] == 'L' and t[1] == t[4] and abs(float(t[5]) - float(t[2])) <= 2


def groove(spec):
    subs = ['M ' + q.strip() for q in spec.split('M ') if q.strip()]
    subs = [q for q in subs if not _is_dot(q)]
    return path(' '.join(subs), GROOVE, 'flat', 'mitre') if subs else Polygon()


def draw():
    shapes = {}
    for c, s in SLAB.items():
        if not s:
            shapes[c] = Polygon()
            continue
        outer = stroked(s, STEM, cap='flat', join='mitre', dot='square')
        shapes[c] = outer.difference(groove(s).intersection(outer.buffer(-RIM)))
    return fit_all(shapes, sb=32, space=260, cell=ADVANCE)
