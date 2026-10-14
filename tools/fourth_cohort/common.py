"""New Fourth Cohort path parser, nibs, treatments and ASCII punctuation.
Copyright (c) 2026 techrote. SIL OFL 1.1; see OFL.txt.
No old alphabet or font file is a drawing input. Only geometry/repertoire
utilities from Original Trio are imported; their repository files are unchanged.
"""
from __future__ import annotations
import math
import sys
from pathlib import Path
from functools import lru_cache
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'original_trio'))
from geometry import (Polygon, LineString, Point, box, polygon, merge, clean,
                      scale, translate, affine_transform, cubic, contours, disc)
from repertoire import extend, COVERAGE, ASCII, BLANKS, BOX_ARMS
from shapely.ops import substring
from masters import rail, gimbal, quoin, pinfeed, camber, octant

MASTERS = {'rail': rail, 'gimbal': gimbal, 'quoin': quoin,
           'pinfeed': pinfeed, 'camber': camber, 'octant': octant}
LETTERS_DIGITS = frozenset('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
FUNCTIONAL = set(BOX_ARMS) | set('█▀▄▌▐░▒▓')

@lru_cache(maxsize=1024)
def paths(spec: str) -> tuple:
    """Strict M/L/C/Z parser returning separate, sampled open/closed polylines."""
    t = spec.split(); parts = []; pts = []; i = 0
    while i < len(t):
        op = t[i]; i += 1
        if op in ('M', 'L'):
            if i + 1 >= len(t): raise ValueError('Truncated coordinate pair')
            xy = tuple(map(float, t[i:i+2])); i += 2
            if op == 'M':
                if len(pts) > 1: parts.append(tuple(pts))
                elif pts: raise ValueError('Isolated source point')
                pts = [xy]
            else:
                if not pts: raise ValueError('L without M')
                pts.append(xy)
        elif op == 'C':
            if not pts or i + 5 >= len(t): raise ValueError('Incomplete cubic')
            controls = [tuple(map(float, t[j:j+2])) for j in range(i, i+6, 2)]
            pts.extend(cubic([pts[-1]] + controls, steps=24)[1:]); i += 6
        elif op == 'Z':
            if len(pts) < 3: raise ValueError('Incomplete closed path')
            pts.append(pts[0])
        else: raise ValueError(f'Unknown path command {op!r}')
    if len(pts) > 1: parts.append(tuple(pts))
    elif pts: raise ValueError('Isolated source point')
    if not parts: raise ValueError('Empty path')
    return tuple(parts)


def nib_line(points, wx: float, wy: float, cap='round', join='round'):
    """Elliptical nib as an affine circle buffer; anisotropy makes stroke contrast."""
    if wx <= 0 or wy <= 0: raise ValueError('Nonpositive nib')
    line = LineString([(x/wx, y/wy) for x,y in points])
    g = line.buffer(.5, quad_segs=10, cap_style=cap, join_style=join)
    return scale(g, xfact=wx, yfact=wy, origin=(0,0))


def nib(spec, wx=76, wy=None, cap='round', join='round'):
    return merge(*(nib_line(p, wx, wx if wy is None else wy, cap, join) for p in paths(spec)))


def fit_horizontal(g, advance: int, margin: int):
    if g.is_empty: return g
    x0,_,x1,_ = g.bounds
    sx = min(1., (advance-2*margin)/(x1-x0))
    g = scale(g, xfact=sx, yfact=1, origin=(0,0))
    x0,_,x1,_ = g.bounds
    return translate(g, xoff=(advance-x1+x0)/2-x0)


def wedge(x, y, width, height, top=False, stem=84):
    """Six-vertex wedge: selected real endpoints only, never every vertex."""
    g = polygon([(x-width/2,y), (x+width/2,y), (x+width/2,y+height*.27),
                 (x+stem/2,y+height), (x-stem/2,y+height), (x-width/2,y+height*.27)])
    return scale(g, xfact=1, yfact=-1, origin=(x,y)) if top else g


PUNCT = {
'.':'M 310 31 L 311 31', ',':'M 333 73 C 335 11 298 -32 271 -66',
':':'M 310 393 L 311 393 M 310 51 L 311 51',
';':'M 310 393 L 311 393 M 333 73 C 335 11 298 -32 271 -66',
'!':'M 311 700 L 311 227 M 310 32 L 311 32',
'?':'M 136 548 C 175 791 518 737 494 552 C 475 411 326 450 311 243 M 310 32 L 311 32',
'"':'M 216 713 L 205 541 M 415 713 L 404 541',
"'":'M 311 713 L 300 541', '`':'M 251 739 L 375 621',
'#':'M 236 710 L 173 -1 M 468 710 L 405 -1 M 102 242 L 535 242 M 124 474 L 555 474',
'$':'M 502 593 C 385 754 123 723 132 547 C 140 375 511 395 503 178 C 496 -28 207 -34 116 100 M 312 -105 L 312 802',
'%':'M 146 8 L 480 702',
'&':'M 548 18 C 456 133 108 432 161 605 C 205 756 454 738 444 580 C 434 403 97 376 105 171 C 113 -60 493 -84 537 291',
'(':'M 400 761 C 95 569 110 114 400 -96',
')':'M 220 761 C 525 569 510 114 220 -96',
'*':'M 310 743 L 310 316 M 104 624 L 516 428 M 104 428 L 516 624',
'+':'M 108 308 L 512 308 M 310 106 L 310 510',
'-':'M 136 308 L 484 308',
'/':'M 115 -80 L 505 765', '\\':'M 115 765 L 505 -80',
'=':'M 115 426 L 505 426 M 115 194 L 505 194',
'<':'M 502 562 L 119 310 L 502 58',
'>':'M 118 562 L 501 310 L 118 58',
'@':'M 470 279 C 457 531 228 489 224 297 C 220 102 449 140 469 354 L 472 208 C 662 97 642 658 340 683 C -1 711 -35 29 336 20 C 449 17 524 63 564 96',
'[':'M 406 760 L 216 760 L 216 -92 L 406 -92',
']':'M 214 760 L 404 760 L 404 -92 L 214 -92',
'^':'M 132 433 L 310 702 L 488 433',
'_':'M 50 -146 L 570 -146',
'{':'M 450 760 C 223 809 310 455 177 355 C 310 255 223 -136 450 -92',
'}':'M 170 760 C 397 809 310 455 443 355 C 310 255 397 -136 170 -92',
'|':'M 310 -140 L 310 789',
'~':'M 112 264 C 247 515 373 101 508 353',
}


def punctuation(width):
    result = {c: nib(spec, width, cap='round') for c,spec in PUNCT.items()}
    # Independent oval percent eyes, deliberately not taken from any font's zero.
    def eye(x,y):
        outer = scale(disc(x,y,90),xfact=.86,yfact=1.12,origin=(x,y))
        inner = scale(disc(x,y,44),xfact=.86,yfact=1.12,origin=(x,y))
        return outer.difference(inner)
    result['%'] = merge(result['%'], eye(176,552), eye(449,153))
    result[' '] = Polygon()
    if set(result) != set(ASCII)-LETTERS_DIGITS: raise ValueError('Incomplete punctuation')
    return result


def stitched(spec, width=44, period=150, on=72):
    """Arclength dashes; deterministic, preserves curves instead of row slicing."""
    parts = []
    for points in paths(spec):
        line = LineString(points)
        n = max(1, math.ceil(line.length/period))
        # Fit a whole number of periods to each separate path: avoid tiny end slivers.
        step = line.length/n
        for i in range(n):
            start = i*step; end = min(line.length, start+step*on/period)
            if end > start:
                seg = substring(line, start, end)
                if seg.geom_type == 'LineString': parts.append(nib_line(seg.coords, width, width, cap='round'))
    return merge(*parts)


def cairn(spec):
    """Place separated tapered stones along each polyline, aligned to its tangent."""
    stones = []
    for points in paths(spec):
        line = LineString(points); n = max(1, math.ceil(line.length/104))
        for i in range(n):
            d = (i+.5)*line.length/n; center = line.interpolate(d)
            a = line.interpolate(max(0,d-1)); b = line.interpolate(min(line.length,d+1))
            dx,dy = b.x-a.x,b.y-a.y; length = math.hypot(dx,dy)
            if length == 0: continue
            ux,uy = dx/length,dy/length; vx,vy = -uy,ux
            half = min(46, .40*line.length/n)
            local = [(0,-43),(half,0),(0,43),(-half,0)]
            stones.append(polygon([(center.x+u*ux+v*vx,center.y+u*uy+v*vy) for u,v in local]))
    return merge(*stones)


def hatch(g):
    if g.is_empty: return g
    # 18-unit continuous silhouette edge + 12-unit diagonal engraving bands.
    border = g.difference(g.buffer(-18, quad_segs=8))
    stripes = merge(*(nib_line([(k,-260),(k+1300,1040)],12,12) for k in range(-1400,1600,58)))
    return merge(border, g.intersection(stripes))


def grid_shape(drawing, woven=False, dot_lift=False):
    parts=[]
    for row,line in enumerate(drawing.split('/')):
        for col,v in enumerate(line):
            if v != '#': continue
            x,y = 80+col*60, 660-(row+1)*60
            if dot_lift and row == 0: y += 2  # Keep i-dot strictly above the shared accent cut.
            if not woven: g = box(x,y,x+60,y+60)
            else:
                g = polygon([(x+3,y+7),(x+54,y+1),(x+59,y+53),(x+7,y+59)])
                slit = box(x+23,y+7,x+35,y+53) if (row+col)%2 else box(x+7,y+23,x+53,y+35)
                g = g.difference(slit)
            parts.append(g)
    return merge(*parts)


def raw_alphabet(cfg):
    m = MASTERS[cfg['lineage']]; treatment = cfg['treatment']; result = {}
    drawings = dict(getattr(m,'PATHS',getattr(m,'GRID',{})))
    drawings.update(cfg.get('overrides', {}))
    if set(drawings) != LETTERS_DIGITS: raise ValueError('Incomplete alphabet')
    for c,spec in drawings.items():
        if cfg['lineage']=='pinfeed': g = grid_shape(spec,treatment=='weave',c=='i')
        elif treatment=='stitch': g = stitched(spec)
        elif treatment=='cairn': g = cairn(spec)
        else:
            g = nib(spec,cfg['nib'][0],cfg['nib'][1],cap=cfg.get('cap','round'),join=cfg.get('join','round'))
            if cfg['lineage']=='quoin':
                serif_width,serif_height = cfg['serif']
                ornaments = [wedge(x,0,serif_width,serif_height,stem=cfg['nib'][0]) for x in quoin.FEET.get(c,[])]
                ornaments += [wedge(x,y,serif_width,serif_height,top=True,stem=cfg['nib'][0]) for x,y in quoin.TOPS.get(c,[])]
                g = merge(g,*ornaments)
            if treatment=='flange':
                flanges=[]
                # Four large attachment tabs only on the long vertical strokes.
                for p in paths(spec):
                    for a,b in zip(p,p[1:]):
                        if abs(a[0]-b[0])<1 and abs(a[1]-b[1])>270:
                            for t in (.08,.92):
                                yy=a[1]+t*(b[1]-a[1])
                                flanges.append(box(a[0]-103,yy-22,a[0]+103,yy+22))
                g=merge(g,*flanges)
            elif treatment=='hatch': g=hatch(g)
        if cfg.get('shear',0): g=affine_transform(g,[1,cfg['shear'],0,1,0,0])
        result[c]=g
    return result


def designs(cfg):
    alphabet = raw_alphabet(cfg)
    core = {**punctuation(cfg['punctuation']), **alphabet}
    sized = {}
    for c,g in core.items():
        if cfg['mono'] or c.isdigit(): a = cfg['advance']
        elif c==' ': a = cfg['space']
        else: a = max(260, int(round(g.bounds[2]-g.bounds[0]+2*cfg['margin'])))
        g = fit_horizontal(g,a,cfg['margin'])
        sized[c] = (clean(g),a)
    # Compose accent bodies before final vertical fitting. This helper remains unchanged.
    extended = extend(sized,cfg['punctuation'],cfg['advance'])
    fitted = {}; adjustments = {}
    for c,(g,a) in extended.items():
        if not g.is_empty and c not in FUNCTIONAL:
            x0,y0,x1,y1=g.bounds
            if y0 < -242 or y1 > 984:
                sy = min(1,1226/(y1-y0))
                g=scale(g,xfact=1,yfact=sy,origin=(0,0))
                dy=max(0,-242-g.bounds[1])+min(0,984-g.bounds[3])
                g=translate(g,yoff=dy)
                adjustments[c]={'scale_y':sy,'translate_y':dy}
        fitted[c]=(clean(g),a)
    return fitted, adjustments
