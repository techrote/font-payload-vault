"""Cleat Inline: heavy condensed capitals with an engraved inline.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Skeleton lineage: CONDENSED (tools/sixth_cohort/lineages.py), treatment drawn here.
"""
from lineages import CONDENSED
from common import stroked, fit_all
from geometry import path, Polygon

FAMILY = 'Cleat Inline'
SLUG = 'cleat-inline'
STEM = 134
ADVANCE = 460
MONO = False
CAP_HEIGHT = 700
X_HEIGHT = 520

INLINE = 30
RIM = 24


def _is_dot(sub):
    t = sub.split()
    return len(t) == 6 and t[3] == 'L' and t[1] == t[4] and abs(float(t[5]) - float(t[2])) <= 2


def groove(spec):
    subs = ['M ' + q.strip() for q in spec.split('M ') if q.strip()]
    subs = [q for q in subs if not _is_dot(q)]
    return path(' '.join(subs), INLINE, 'flat', 'bevel') if subs else Polygon()


def draw():
    shapes = {}
    for c, s in CONDENSED.items():
        if not s:
            shapes[c] = Polygon()
            continue
        outer = stroked(s, STEM, cap='flat', join='bevel', dot='square')
        # Dots stay solid; strokes get a groove that stops short of the edge.
        shapes[c] = outer.difference(groove(s).intersection(outer.buffer(-RIM)))
    return fit_all(shapes, sb=40, space=200, cell=ADVANCE)
