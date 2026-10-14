"""Shared helpers for the Sixth Cohort treatments (stroking, dots, ink-fitting).
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
"""
from geometry import path, merge, box, disc, translate, Polygon

DIGITS = '0123456789'


def stroked(spec, width, cap='flat', join='round', dot='square'):
    """Stroke a skeleton; one-unit segments become dots (round or square)."""
    out = []
    for chunk in spec.split('M '):
        chunk = chunk.strip()
        if not chunk:
            continue
        t = ('M ' + chunk).split()
        if len(t) == 6 and t[3] == 'L' and t[1] == t[4] and abs(float(t[5]) - float(t[2])) <= 2:
            x, y = float(t[1]), float(t[2]) + 0.5
            if dot == 'round':
                out.append(disc(x, y, width * 0.55))
            else:
                out.append(box(x - width / 2, y - width / 2, x + width / 2, y + width / 2))
        else:
            out.append(path('M ' + chunk, width, cap, join))
    return merge(*out)


def fit_all(shapes, sb, space, cell=None):
    """Ink-fit spacing: sb bearings, optional tabular digit cell, fixed space."""
    out = {}
    for c, g in shapes.items():
        if c == ' ':
            out[c] = (Polygon(), space)
            continue
        x0, _, x1, _ = g.bounds
        if cell and c in DIGITS:
            out[c] = (translate(g, (cell - (x0 + x1)) / 2), cell)
        else:
            out[c] = (translate(g, sb - x0), int(round(x1 - x0)) + 2 * sb)
    assert set(out) == {chr(i) for i in range(32, 127)}
    return out
