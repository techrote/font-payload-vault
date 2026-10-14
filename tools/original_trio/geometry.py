"""Original Trio geometry; no font import, tracing, or installed-font lookup.
Copyright (c) 2026 techrote. SIL Open Font License 1.1; see OFL.txt.
"""
from __future__ import annotations
import math
from shapely import Polygon, MultiPolygon, GeometryCollection, LineString, Point, box, set_precision
from shapely.ops import unary_union
from shapely.geometry.polygon import orient
from shapely.affinity import translate, scale, affine_transform


def merge(*parts):
    return unary_union([p for p in parts if p is not None and not p.is_empty])


def polygon(points):
    return Polygon(points)


def stroke(points, width=72, cap='flat', join='round'):
    return LineString(points).buffer(width / 2, quad_segs=12, cap_style=cap, join_style=join)


def disc(x, y, r):
    return Point(x, y).buffer(r, quad_segs=12)


def cubic(points, steps=20):
    """Sample an explicitly authored cubic; later snapped to integer font units."""
    a, b, c, d = points
    return [tuple((1-t)**3*a[k] + 3*(1-t)**2*t*b[k] + 3*(1-t)*t*t*c[k] + t**3*d[k]
                  for k in (0, 1)) for t in [i/steps for i in range(steps+1)]]


def path(spec, width=72, cap='flat', join='round'):
    """Compact source path: M x y; L x y; C x1 y1 x2 y2 x y; Z."""
    tokens = spec.replace(',', ' ').split()
    result, points, i = [], [], 0
    while i < len(tokens):
        cmd = tokens[i]; i += 1
        if cmd in ('M', 'L'):
            p = (float(tokens[i]), float(tokens[i+1])); i += 2
            if cmd == 'M' and points:
                result.append(stroke(points, width, cap, join)); points = []
            points.append(p)
        elif cmd == 'C':
            if not points:
                raise ValueError('C without initial M')
            p = [tuple(map(float, tokens[j:j+2])) for j in range(i, i+6, 2)]
            i += 6
            points.extend(cubic([points[-1]] + p)[1:])
        elif cmd == 'Z':
            points.append(points[0])
        else:
            raise ValueError(f'Unknown path command: {cmd}')
    if points:
        result.append(stroke(points, width, cap, join))
    return merge(*result)


def chamfer(x0, y0, x1, y1, c=55):
    c = min(c, (x1-x0)/2, (y1-y0)/2)
    return polygon([(x0+c,y0),(x1-c,y0),(x1,y0+c),(x1,y1-c),
                    (x1-c,y1),(x0+c,y1),(x0,y1-c),(x0,y0+c)])


def polygons(g):
    if g.is_empty:
        return []
    if isinstance(g, Polygon):
        return [g]
    if isinstance(g, (MultiPolygon, GeometryCollection)):
        return [p for part in g.geoms for p in polygons(part)]
    raise ValueError(f'Non-area geometry: {g.geom_type}')


def clean(g):
    if g.is_empty:
        return Polygon()
    if not g.is_valid:
        raise ValueError('Invalid source geometry')
    g = set_precision(g, grid_size=1.0, mode='valid_output').normalize()
    if not g.is_valid:
        raise ValueError('Invalid quantized geometry')
    return g


def contours(g):
    """Deterministic clockwise exteriors / anticlockwise counters for TrueType."""
    rings = []
    for p in sorted(polygons(clean(g)), key=lambda p: (p.bounds, p.wkb)):
        p = orient(p, sign=-1.0)
        for ring in [p.exterior, *p.interiors]:
            xy = [tuple(map(int, pt)) for pt in list(ring.coords)[:-1]]
            start = min(range(len(xy)), key=lambda i: xy[i:]+xy[:i])
            rings.append(xy[start:]+xy[:start])
    return rings


def svg_path(g):
    return ' '.join('M'+' L'.join(f'{x} {y}' for x,y in pts)+' Z' for pts in contours(g))
