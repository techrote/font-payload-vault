"""KNURLED SWARF pixel font — glyph engine.

Hand-drawn masters (M5, M7) are parsed from text grids. Intermediate masters are
derived by inserting rows/columns at the 'quietest' place in each glyph (single
pixel stems rather than bars), steered by per-glyph hints. Per-pixel-size cells
are then assembled, accented letters composed, and procedural glyphs (box
drawing, blocks, shades) generated to fill the exact cell.
"""
import os, re, copy

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- data model
class Glyph:
    def __init__(self, rows, adv=None, hints=None, mode='cap'):
        self.rows = rows            # list[list[int]] — full design box
        self.adv = adv              # explicit advance (space), else width+1
        self.hints = hints or {}
        self.mode = mode
    @property
    def w(self):
        return len(self.rows[0]) if self.rows else 0
    @property
    def h(self):
        return len(self.rows)
    def copy(self):
        return Glyph([r[:] for r in self.rows], self.adv, dict(self.hints), self.mode)

class Master:
    def __init__(self, name, cap, x, desc):
        self.name, self.cap, self.x, self.desc = name, cap, x, desc
        self.glyphs = {}
    @property
    def H(self):
        return self.cap + self.desc

def parse_master(path, name, cap, x, desc):
    m = Master(name, cap, x, desc)
    cur = None
    def flush():
        if cur is None:
            return
        ch, hints, lines = cur
        mode = hints.pop('mode', None)
        adv = int(hints.pop('w')) if 'w' in hints else None
        if ch == 'space':
            ch = ' '
            rows = [[0] * 0 for _ in range(m.H)]
            g = Glyph([[] for _ in range(m.H)], adv=adv)
            m.glyphs[ch] = g
            return
        if len(lines) > m.H:
            raise ValueError(f'{name} {ch!r}: {len(lines)} rows > {m.H}')
        w = max(len(l) for l in lines)
        rows = [[1 if c == '#' else 0 for c in l.ljust(w, '.')] for l in lines]
        while len(rows) < m.H:
            rows.append([0] * w)
        if mode is None:
            mode = 'lower' if (ch.islower() or ch in 'ßµ') else 'cap'
        m.glyphs[ch] = Glyph(rows, adv, hints, mode)
    with open(path, encoding='utf-8') as f:
        for raw in f:
            line = raw.rstrip('\n').rstrip()
            if not line or line.startswith('# ') or line == '#' and cur is None:
                if line.startswith('# ') or line == '':
                    continue
            if line.startswith('@ '):
                flush()
                parts = line[2:].split()
                ch = parts[0]
                if ch.startswith('U+'):
                    ch = chr(int(ch[2:], 16))
                hints = {}
                for p in parts[1:]:
                    k, v = p.split('=', 1)
                    hints[k] = v
                cur = (ch, hints, [])
            elif cur is not None:
                if not re.fullmatch(r'[#.]+', line):
                    raise ValueError(f'{name} {cur[0]!r}: bad row {line!r}')
                cur[2].append(line)
    flush()
    return m

# ------------------------------------------------------------ derivation
def maxrun(seq):
    best = run = 0
    for v in seq:
        run = run + 1 if v else 0
        best = max(best, run)
    return best

def _insert_rows(rows, origin, lo, hi, count, hint, dupcount, prefer_center):
    """Insert `count` rows inside region [lo, hi) of `rows` (region grows)."""
    for _ in range(count):
        H = len(rows)
        region_has_ink = any(any(rows[i]) for i in range(lo, hi))
        if not region_has_ink:
            rows.insert(lo, [0] * len(rows[0])); origin.insert(lo, None)
            hi += 1
            continue
        choice = None
        while hint:
            item = hint.pop(0)
            if item == 't':
                rows.insert(lo, [0] * len(rows[0])); origin.insert(lo, None)
                choice = 'done'; break
            if item == 'b':
                rows.insert(hi, [0] * len(rows[0])); origin.insert(hi, None)
                choice = 'done'; break
            src = int(item)
            idx = [i for i in range(lo, hi) if origin[i] == src]
            if idx:
                choice = idx[-1]; break
        if choice == 'done':
            hi += 1
            continue
        if choice is None:
            best = None
            for i in range(lo, hi):
                row = rows[i]
                run = maxrun(row)
                blank = not any(row)
                above = any(any(r) for r in rows[:i])
                below = any(any(r) for r in rows[i + 1:])
                s = 0.0
                if run >= 2:
                    s += 10 + run
                if blank:
                    s += 6 if (above and below) else 1.5
                eq = (i > lo and rows[i - 1] == row) or (i + 1 < hi and rows[i + 1] == row)
                if not eq and not blank:
                    s += 2
                s += 0.6 * abs(i - prefer_center(lo, hi))
                s += 4 * dupcount.get(origin[i], 0)
                s -= 0.01 * i            # tie-break: lower row wins
                if best is None or s < best[0]:
                    best = (s, i)
            choice = best[1]
        rows.insert(choice + 1, rows[choice][:])
        origin.insert(choice + 1, origin[choice])
        dupcount[origin[choice]] = dupcount.get(origin[choice], 0) + 1
        hi += 1
    return hi

def _widen(rows, count, hint):
    if count <= 0:
        return rows
    cols = [list(c) for c in zip(*rows)]
    origin = list(range(len(cols)))
    dup = {}
    sym = all(r == r[::-1] for r in rows)
    for _ in range(count):
        W = len(cols)
        choice = None
        while hint:
            src = int(hint.pop(0))
            idx = [i for i in range(W) if origin[i] == src]
            if idx:
                choice = idx[-1]; break
        if choice is None:
            best = None
            center = (W - 1) / 2
            for i in range(W):
                c = cols[i]
                run = maxrun(c)
                s = 0.0
                if run >= 3:
                    s += 20 + run          # never fatten a 1px stem
                for y, v in enumerate(c):  # isolated pixels: dots / stroke ends
                    if v and not (i > 0 and cols[i - 1][y]) and not (i + 1 < W and cols[i + 1][y]):
                        s += 2
                if not any(c):
                    s += 3
                if sym and i == center:
                    s -= 5
                eq = (i > 0 and cols[i - 1] == c) or (i + 1 < W and cols[i + 1] == c)
                if eq:
                    s -= 1
                s += 1.0 * abs(i - center)
                s += 3 * dup.get(origin[i], 0)
                if best is None or s < best[0]:
                    best = (s, i)
            choice = best[1]
        cols.insert(choice + 1, cols[choice][:])
        origin.insert(choice + 1, origin[choice])
        dup[origin[choice]] = dup.get(origin[choice], 0) + 1
    return [list(r) for r in zip(*cols)]

def _hint(g, key, tname):
    v = g.hints.get(f'{key}.{tname}', g.hints.get(key))
    if v is None:
        return []
    return [p for p in v.split(',') if p != '']

MATH_CENTER = set('-+=×÷<>~‹›«»•·–—¬')

def recenter(rows, cap, x):
    top, bot = ink_top(rows), ink_bottom(rows)
    if bot < 0:
        return rows
    c = (cap - x) + (x - 1) / 2
    shift = int((c - (top + bot) / 2) // 1) if (c - (top + bot) / 2) >= 0 else -int((-(c - (top + bot) / 2)) // 1 + (1 if (-(c - (top + bot) / 2)) % 1 else 0))
    if shift == 0:
        return rows
    W = len(rows[0])
    out = [[0] * W for _ in rows]
    for i, r in enumerate(rows):
        j = i + shift
        if 0 <= j < len(rows):
            out[j] = r[:]
    return out

NO_WIDEN = set('"\'`´¨‘’“”‚„,;:.!|¦¡·•')

def derive(src, tname, cap, x, desc, widen=0, min_widen_w=4):
    t = Master(tname, cap, x, desc)
    for ch, g in src.glyphs.items():
        if ch == ' ':
            t.glyphs[ch] = Glyph([[] for _ in range(t.H)], adv=(g.adv or 2) + widen)
            continue
        rows = [r[:] for r in g.rows]
        auto = widen if (g.w >= min_widen_w and ch not in NO_WIDEN) else 0
        wc = int(g.hints.get(f'wc.{tname}', g.hints.get('wc', auto)))
        if wc:
            rows = _widen(rows, wc, _hint(g, 'xw', tname))
        origin = list(range(len(rows)))
        dup = {}
        # descender region
        dd = desc - src.desc
        dlo, dhi = src.cap, src.cap + src.desc
        if dd > 0:
            has = any(any(rows[i]) for i in range(dlo, dhi))
            if has:
                _insert_rows(rows, origin, src.cap - 1, dhi, dd, _hint(g, 'yd', tname), dup,
                             lambda lo, hi: hi - 1)
            else:
                for _ in range(dd):
                    rows.append([0] * len(rows[0])); origin.append(None)
        if g.mode == 'lower':
            sa, sx = src.cap - src.x, src.x
            ta, tx = cap - x, x
            # x region
            if tx - sx > 0:
                _insert_rows(rows, origin, sa, sa + sx, tx - sx, _hint(g, 'yx', tname), dup,
                             lambda lo, hi: (lo + hi - 1) / 2)
            if ta - sa > 0:
                if any(any(rows[i]) for i in range(0, sa)):
                    _insert_rows(rows, origin, 0, sa, ta - sa, _hint(g, 'ya', tname), dup,
                                 lambda lo, hi: (lo + hi - 1) / 2)
                else:
                    for _ in range(ta - sa):
                        rows.insert(0, [0] * len(rows[0])); origin.insert(0, None)
        else:
            dc = cap - src.cap
            if dc > 0:
                _insert_rows(rows, origin, 0, src.cap, dc, _hint(g, 'yc', tname), dup,
                             lambda lo, hi: (lo + hi - 1) / 2)
        assert len(rows) == t.H, (tname, ch, len(rows), t.H)
        if ch in MATH_CENTER:
            rows = recenter(rows, cap, x)
        ng = Glyph(rows, g.adv, {}, g.mode)
        t.glyphs[ch] = ng
    return t

def apply_overrides(m, path):
    if not os.path.exists(path):
        return
    o = parse_master(path, m.name, m.cap, m.x, m.desc)
    for ch, g in o.glyphs.items():
        m.glyphs[ch] = g

# ------------------------------------------------------------- masters
MASTER_SPECS = {
    'M5':  dict(hand='m5.txt', cap=5, x=4, desc=1),
    'M6':  dict(src='M5', cap=6, x=4, desc=2, widen=0),
    'M7':  dict(hand='m7.txt', cap=7, x=5, desc=2),
    'M8':  dict(src='M7', cap=8, x=6, desc=2, widen=0),
    'M9':  dict(src='M7', cap=9, x=7, desc=3, widen=1),
    'M10': dict(src='M7', cap=10, x=7, desc=3, widen=1),
    'M11': dict(src='M7', cap=11, x=8, desc=3, widen=2),
}

# ppem -> (master, ascent rows above baseline, descent rows)
SIZES = {
    6:  ('M5', 5, 1),
    7:  ('M5', 6, 1),
    8:  ('M6', 6, 2),
    9:  ('M6', 7, 2),
    10: ('M7', 8, 2),
    11: ('M8', 9, 2),
    12: ('M8', 10, 2),
    13: ('M9', 10, 3),
    14: ('M10', 11, 3),
    15: ('M10', 12, 3),
    16: ('M11', 13, 3),
}

def load_masters():
    ms = {}
    for name, spec in MASTER_SPECS.items():
        if 'hand' in spec:
            ms[name] = parse_master(os.path.join(HERE, spec['hand']), name,
                                    spec['cap'], spec['x'], spec['desc'])
    for name, spec in MASTER_SPECS.items():
        if 'src' in spec:
            ms[name] = derive(ms[spec['src']], name, spec['cap'], spec['x'], spec['desc'],
                              spec['widen'])
        apply_overrides(ms[name], os.path.join(HERE, f'{name.lower()}.over.txt'))
    return ms

# ------------------------------------------------------- per-size cells
class Cell:
    """A glyph bitmap positioned in a ppem cell. rows cover the full cell height."""
    def __init__(self, rows, adv, lsb=0):
        self.rows = rows      # cell-height rows, width = bitmap width
        self.adv = adv
        self.lsb = lsb        # left side bearing in px (bitmap x offset)
    @property
    def w(self):
        return len(self.rows[0]) if self.rows else 0

def blank(w, h):
    return [[0] * w for _ in range(h)]

def bmp(lines):
    return [[1 if c == '#' else 0 for c in l] for l in lines]

ACCENTS = {
    'grave':     [['#.', '.#'], ['#.']],
    'acute':     [['.#', '#.'], ['.#']],
    'circ':      [['.#.', '#.#'], ['.#.']],
    'caron':     [['#.#', '.#.'], ['.#.']],
    'tilde':     [['.#.#', '#.#.'], ['.##', '##.'], ['###']],
    'ring':      [['.#.', '#.#', '.#.'], ['##', '##'], ['.#.']],
    'dier':      None,   # width dependent
}
CEDILLA = [['.#.', '##.'], ['.#.']]

COMPOSE = {
    'À': ('A', 'grave'), 'Á': ('A', 'acute'), 'Â': ('A', 'circ'), 'Ã': ('A', 'tilde'),
    'Ä': ('A', 'dier'), 'Å': ('A', 'ring'), 'È': ('E', 'grave'), 'É': ('E', 'acute'),
    'Ê': ('E', 'circ'), 'Ë': ('E', 'dier'), 'Ì': ('I', 'grave'), 'Í': ('I', 'acute'),
    'Î': ('I', 'circ'), 'Ï': ('I', 'dier'), 'Ñ': ('N', 'tilde'), 'Ò': ('O', 'grave'),
    'Ó': ('O', 'acute'), 'Ô': ('O', 'circ'), 'Õ': ('O', 'tilde'), 'Ö': ('O', 'dier'),
    'Ù': ('U', 'grave'), 'Ú': ('U', 'acute'), 'Û': ('U', 'circ'), 'Ü': ('U', 'dier'),
    'Ý': ('Y', 'acute'), 'Ÿ': ('Y', 'dier'), 'Š': ('S', 'caron'), 'Ž': ('Z', 'caron'),
    'à': ('a', 'grave'), 'á': ('a', 'acute'), 'â': ('a', 'circ'), 'ã': ('a', 'tilde'),
    'ä': ('a', 'dier'), 'å': ('a', 'ring'), 'è': ('e', 'grave'), 'é': ('e', 'acute'),
    'ê': ('e', 'circ'), 'ë': ('e', 'dier'), 'ì': ('ı', 'grave'), 'í': ('ı', 'acute'),
    'î': ('ı', 'circ'), 'ï': ('ı', 'dier'), 'ñ': ('n', 'tilde'), 'ò': ('o', 'grave'),
    'ó': ('o', 'acute'), 'ô': ('o', 'circ'), 'õ': ('o', 'tilde'), 'ö': ('o', 'dier'),
    'ù': ('u', 'grave'), 'ú': ('u', 'acute'), 'û': ('u', 'circ'), 'ü': ('u', 'dier'),
    'ý': ('y', 'acute'), 'ÿ': ('y', 'dier'), 'š': ('s', 'caron'), 'ž': ('z', 'caron'),
}

def dier_for(w):
    if w >= 5:
        pat = '.#.#.' if w % 2 else '#..#'
    elif w == 4:
        pat = '#..#'
    else:
        pat = '#.#'
    return [[pat]]

def ink_top(rows):
    for i, r in enumerate(rows):
        if any(r):
            return i
    return len(rows)

def ink_bottom(rows):
    for i in range(len(rows) - 1, -1, -1):
        if any(rows[i]):
            return i
    return -1

def squash_one(rows, top, bottom):
    """Remove the most redundant row in [top, bottom]; rows above shift down."""
    best = None
    for i in range(top, bottom + 1):
        r = rows[i]
        s = 0.0
        if maxrun(r) >= 2: s += 10
        eq = (rows[i - 1] == r) or (i + 1 < len(rows) and rows[i + 1] == r)
        if not eq: s += 3
        s += 0.3 * abs(i - (top + bottom) / 2)
        if best is None or s < best[0]:
            best = (s, i)
    i = best[1]
    del rows[i]
    rows.insert(0, [0] * len(rows[0]))

def place(rows, acc, top_row, w):
    """Overlay accent bitmap `acc` with its top at top_row, centred over width w."""
    aw = len(acc[0])
    W = max(w, aw)
    pad_l = (W - w) // 2
    out = [[0] * pad_l + r + [0] * (W - w - pad_l) for r in rows]
    ax = (W - aw) // 2 if aw <= w else 0
    for j, ar in enumerate(acc):
        for i, v in enumerate(ar):
            if v:
                out[top_row + j][ax + i] = 1
    return out

def compose_accent(base_rows, accent, lower):
    w = len(base_rows[0])
    variants = dier_for(w) if accent == 'dier' else ACCENTS[accent]
    variants = [bmp(v) for v in variants]
    # prefer variants no wider than the base
    variants = sorted(variants, key=lambda v: (len(v[0]) > max(w, 3),))
    rows = [r[:] for r in base_rows]
    for gap in (1, 0):
        for v in variants:
            if len(v[0]) > max(w, 3) and accent != 'dier':
                continue
            t = ink_top(rows)
            if t - gap - len(v) >= 0:
                return place(rows, v, t - gap - len(v), w)
    # no room: squash the base and use the smallest variant with no gap
    v = min(variants, key=len)
    while ink_top(rows) - len(v) < 0:
        squash_one(rows, ink_top(rows), ink_bottom(rows))
    return place(rows, v, ink_top(rows) - len(v), w)

def compose_cedilla(base_rows, baseline):
    w = len(base_rows[0])
    rows = [r[:] for r in base_rows]
    avail = len(rows) - baseline
    for v in CEDILLA:
        v = bmp(v)
        if len(v) <= avail:
            return place(rows, v, baseline, w)
    return rows

def overlay_slash(rows, top, bottom):
    w = len(rows[0])
    rows = [r[:] for r in rows]
    n = bottom - top
    for k in range(n + 1):
        y = bottom - k
        x = round(k * (w - 1) / n) if n else 0
        rows[y][x] = 1
    return rows

def build_size(ms, ppem):
    mname, asc, dsc = SIZES[ppem]
    m = ms[mname]
    assert dsc == m.desc, (ppem, dsc, m.desc)
    H = asc + dsc
    off = asc - m.cap
    cells = {}
    for ch, g in m.glyphs.items():
        rows = blank(g.w, H)
        for i, r in enumerate(g.rows):
            rows[off + i] = r[:]
        adv = g.adv if g.adv is not None else g.w + 1
        cells[ch] = Cell(rows, adv)
    baseline = asc  # first descender row index
    # dotless i
    i_rows = [r[:] for r in cells['i'].rows]
    xtop = asc - m.x
    for k in range(0, xtop):
        i_rows[k] = [0] * len(i_rows[k])
    # keep only the x-height stem
    cells['ı'] = Cell(i_rows, cells['i'].adv)
    for ch, (base, acc) in COMPOSE.items():
        b = cells[base]
        rows = compose_accent(b.rows, acc, base.islower() or base == 'ı')
        cells[ch] = Cell(rows, len(rows[0]) + 1)
    cells['Ç'] = Cell(compose_cedilla(cells['C'].rows, baseline), cells['C'].adv)
    cells['ç'] = Cell(compose_cedilla(cells['c'].rows, baseline), cells['c'].adv)
    for ch, base in (('Ø', 'O'), ('ø', 'o')):
        b = cells[base]
        cells[ch] = Cell(overlay_slash(b.rows, ink_top(b.rows), ink_bottom(b.rows)), b.adv)
    # Ð : D shifted right with a bar through the stem
    d = cells['D']
    rows = [[0] + r for r in d.rows]
    mid = (ink_top(rows) + ink_bottom(rows)) // 2
    for xx in range(0, 3):
        rows[mid][xx] = 1
    cells['Ð'] = Cell(rows, len(rows[0]) + 1)
    # non-breaking space / soft hyphen
    cells[' '] = Cell([[] for _ in range(H)], cells[' '].adv)
    cells['­'] = cells['-']
    add_procedural(cells, ppem, asc, dsc, m)
    return cells

# ------------------------------------------------------ procedural glyphs
BOX = {
    # char: (up, down, left, right) with 1=light, 2=double
    '─': (0, 0, 1, 1), '│': (1, 1, 0, 0), '┌': (0, 1, 0, 1), '┐': (0, 1, 1, 0),
    '└': (1, 0, 0, 1), '┘': (1, 0, 1, 0), '├': (1, 1, 0, 1), '┤': (1, 1, 1, 0),
    '┬': (0, 1, 1, 1), '┴': (1, 0, 1, 1), '┼': (1, 1, 1, 1),
    '═': (0, 0, 2, 2), '║': (2, 2, 0, 0), '╔': (0, 2, 0, 2), '╗': (0, 2, 2, 0),
    '╚': (2, 0, 0, 2), '╝': (2, 0, 2, 0), '╠': (2, 2, 0, 2), '╣': (2, 2, 2, 0),
    '╦': (0, 2, 2, 2), '╩': (2, 0, 2, 2), '╬': (2, 2, 2, 2),
    '╒': (0, 1, 0, 2), '╕': (0, 1, 2, 0), '╘': (1, 0, 0, 2), '╛': (1, 0, 2, 0),
    '╓': (0, 2, 0, 1), '╖': (0, 2, 1, 0), '╙': (2, 0, 0, 1), '╜': (2, 0, 1, 0),
    '╞': (1, 1, 0, 2), '╡': (1, 1, 2, 0), '╟': (2, 2, 0, 1), '╢': (2, 2, 1, 0),
    '╤': (0, 1, 2, 2), '╧': (1, 0, 2, 2), '╥': (0, 2, 1, 1), '╨': (2, 0, 1, 1),
    '╪': (1, 1, 2, 2), '╫': (2, 2, 1, 1),
    '╴': (0, 0, 1, 0), '╵': (1, 0, 0, 0), '╶': (0, 0, 0, 1), '╷': (0, 1, 0, 0),
}

def box_glyph(W, H, up, dn, lf, rt):
    g = blank(W, H)
    cx, cy = (W - 1) // 2, (H - 1) // 2
    L, R, T, B = cx - 1, cx + 1, cy - 1, cy + 1
    def vl(x, y0, y1):
        for y in range(max(0, min(y0, y1)), min(H - 1, max(y0, y1)) + 1):
            g[y][x] = 1
    def hl(y, x0, x1):
        for x in range(max(0, min(x0, x1)), min(W - 1, max(x0, x1)) + 1):
            g[y][x] = 1
    vd = max(up, dn) == 2
    hd = max(lf, rt) == 2
    hany, vany = bool(lf or rt), bool(up or dn)
    # ---- vertical arms
    for arm, on in (('up', up), ('dn', dn)):
        if not on:
            continue
        edge = 0 if arm == 'up' else H - 1
        other = dn if arm == 'up' else up
        if vd:
            for side, x in (('L', L), ('R', R)):
                if hd:
                    mine = lf if side == 'L' else rt
                    opp = rt if side == 'L' else lf
                    if mine:
                        stop = T if arm == 'up' else B
                    elif other:
                        stop = cy
                    elif opp:
                        stop = B if arm == 'up' else T
                    else:
                        stop = cy
                else:
                    stop = cy
                vl(x, edge, stop)
        else:
            if hd:
                through = lf and rt
                if other:
                    stop = cy
                elif through:
                    stop = T if arm == 'up' else B      # T-junction: nearer line
                else:
                    stop = B if arm == 'up' else T      # corner: farther line
            else:
                stop = cy
            vl(cx, edge, stop)
    # ---- horizontal arms
    for arm, on in (('lf', lf), ('rt', rt)):
        if not on:
            continue
        edge = 0 if arm == 'lf' else W - 1
        other = rt if arm == 'lf' else lf
        if hd:
            for side, y in (('T', T), ('B', B)):
                if vd:
                    mine = up if side == 'T' else dn
                    opp = dn if side == 'T' else up
                    if mine:
                        stop = L if arm == 'lf' else R
                    elif other:
                        stop = cx
                    elif opp:
                        stop = R if arm == 'lf' else L
                    else:
                        stop = cx
                else:
                    stop = cx
                hl(y, edge, stop)
        else:
            if vd:
                through = up and dn
                if other:
                    stop = cx
                elif through:
                    stop = L if arm == 'lf' else R
                else:
                    stop = R if arm == 'lf' else L
            else:
                stop = cx
            hl(cy, edge, stop)
    return g

def add_procedural(cells, ppem, asc, dsc, m):
    H = asc + dsc
    W = cells['0'].adv  # box cell = digit advance (tabular)
    for ch, spec in BOX.items():
        cells[ch] = Cell(box_glyph(W, H, *spec), W)
    # rounded corners
    for ch, base, (dy, dx) in (('╭', '┌', (1, 1)), ('╮', '┐', (1, -1)),
                               ('╯', '┘', (-1, -1)), ('╰', '└', (-1, 1))):
        g = [r[:] for r in cells[base].rows]
        cx, cy = (W - 1) // 2, (H - 1) // 2
        g[cy][cx] = 0
        g[cy + dy][cx] = 1 if False else g[cy + dy][cx]
        g[cy][cx + dx] = g[cy][cx + dx]
        g[cy + dy][cx + dx] = 1
        g[cy + dy][cx] = 0
        g[cy][cx + dx] = 0
        cells[ch] = Cell(g, W)
    full = [[1] * W for _ in range(H)]
    cells['█'] = Cell(full, W)
    half = H // 2
    cells['▀'] = Cell([[1] * W if y < half else [0] * W for y in range(H)], W)
    cells['▄'] = Cell([[1] * W if y >= half else [0] * W for y in range(H)], W)
    cells['▌'] = Cell([[1 if x < W // 2 else 0 for x in range(W)] for y in range(H)], W)
    cells['▐'] = Cell([[1 if x >= W // 2 else 0 for x in range(W)] for y in range(H)], W)
    cells['░'] = Cell([[1 if (y % 2 == 0 and x % 2 == (y // 2) % 2) else 0 for x in range(W)]
                       for y in range(H)], W)
    cells['▒'] = Cell([[1 if (x + y) % 2 == 0 else 0 for x in range(W)] for y in range(H)], W)
    cells['▓'] = Cell([[0 if (y % 2 == 0 and x % 2 == (y // 2) % 2) else 1 for x in range(W)]
                       for y in range(H)], W)
    # geometric shapes sized to the x-height
    s = m.x if m.x % 2 else m.x - 1
    s = max(3, s)
    xtop = asc - m.x
    y0 = xtop + (m.x - s) // 2
    def shape(fn, size, yoff):
        rows = blank(size, H)
        for j in range(size):
            for i in range(size):
                if fn(i, j, size):
                    rows[yoff + j][i] = 1
        return Cell(rows, size + 1)
    cells['■'] = shape(lambda i, j, n: True, s, y0)
    cells['□'] = shape(lambda i, j, n: i in (0, n - 1) or j in (0, n - 1), s, y0)
    sm = max(2, s - 2)
    cells['▪'] = shape(lambda i, j, n: True, sm, y0 + (s - sm) // 2)
    cells['▫'] = shape(lambda i, j, n: i in (0, n - 1) or j in (0, n - 1), sm, y0 + (s - sm) // 2)
    def circ_fill(i, j, n):
        c = (n - 1) / 2
        return (i - c) ** 2 + (j - c) ** 2 <= (n / 2) ** 2
    def circ_ring(i, j, n):
        if not circ_fill(i, j, n):
            return False
        if i in (0, n - 1) or j in (0, n - 1):
            return True
        return not circ_fill(i - 1, j - 1, n - 2)
    cells['●'] = shape(circ_fill, s, y0)
    cells['○'] = shape(circ_ring, s, y0)

def embolden(rows):
    """VGA-style horizontal smear; first open every 1px counter so it survives."""
    W = len(rows[0])
    gaps = [c for c in range(1, W - 1)
            if any(r[c - 1] and not r[c] and r[c + 1] for r in rows)]
    if gaps:
        out = []
        for r in rows:
            nr = []
            for c, v in enumerate(r):
                nr.append(v)
                if c in gaps:
                    nr.append(v)
            out.append(nr)
        rows = out
    res = []
    for r in rows:
        nr = r + [0]
        res.append([nr[i] | (nr[i - 1] if i > 0 else 0) for i in range(len(nr))])
    return res

def bold_cells(cells, skip):
    out = {}
    for ch, c in cells.items():
        if ch in skip or not c.rows or not c.rows[0]:
            extra = 0 if (ch in skip or not c.rows or not c.rows[0]) else 1
            out[ch] = Cell([r[:] for r in c.rows], c.adv + (1 if ch in (' ', '\u00a0') else 0))
            continue
        rows = embolden(c.rows)
        out[ch] = Cell(rows, len(rows[0]) + 1)
    return out

PROCEDURAL = set(BOX) | set('╭╮╯╰█▀▄▌▐░▒▓')

def all_sizes(ms=None):
    ms = ms or load_masters()
    reg = {p: build_size(ms, p) for p in SIZES}
    bold = {p: bold_cells(c, PROCEDURAL | set('■□▪▫●○')) for p, c in reg.items()}
    return ms, reg, bold
