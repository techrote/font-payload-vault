"""Build all BLUED SWARF font files from the glyph engine.

Outputs (in ../fonts):
  BluedSwarf-Regular.ttf / -Bold.ttf               universal: outlines (10px design) + bitmap strikes 6-16px
  per-size/BluedSwarf{N}px-*.ttf                   one pixel-exact font per size (outline + its own strike)
  web/BluedSwarf{N}px-*.woff2                      same, for browsers
  windows-fon/BluedSwarfSys.fon / -Bold.fon        Windows raster font library, sizes 6-16 in one file
  bdf/BluedSwarf-{N}px-*.bdf                       X11/Linux/tool-friendly bitmap sources
"""
import os, sys, struct, datetime
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import newTable
from fontTools.ttLib.tables.DefaultTable import DefaultTable
from fontTools import agl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import swarf

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fonts')
FAMILY = 'Blued Swarf'
STEM = 'BluedSwarf'                  # file-name stem
FON_FACE = 'Blued Swarf Sys'          # raster face name (kept distinct from the TrueType family)
FON_FILES = ('BluedSwarfSys.fon', 'BluedSwarfSys-Bold.fon')
VERSION = '1.000'
COPYRIGHT = 'Copyright (c) 2026 techrote'
VENDOR = 'TRTE'
PX = 128                      # font units per pixel in every outline
DESIGN_PPEM = 10              # universal font outlines come from the 10px design

# ------------------------------------------------------------- helpers
def gname(ch):
    if ch == '.notdef':
        return ch
    cp = ord(ch)
    n = agl.UV2AGL.get(cp)
    return n if n else f'uni{cp:04X}'

def notdef_cell(cells, ppem):
    mname, asc, dsc = swarf.SIZES[ppem]
    H = asc + dsc
    zero = cells['0']
    w = max(3, zero.w)
    top = ink_top_of(cells['H'])
    bot = asc - 1
    rows = swarf.blank(w, H)
    for y in range(top, bot + 1):
        for x in range(w):
            if y in (top, bot) or x in (0, w - 1):
                rows[y][x] = 1
    return swarf.Cell(rows, w + 1)

def ink_top_of(cell):
    return swarf.ink_top(cell.rows)

def charset(cells_by_size):
    sets = [set(c) for c in cells_by_size.values()]
    common = set.intersection(*sets)
    assert all(s == common for s in sets), 'glyph coverage differs between sizes'
    return sorted(common, key=ord)

def outline_glyph(cell, asc, unit):
    """Pixel union -> clockwise TrueType contours (holes counter-clockwise)."""
    rows = cell.rows
    H = len(rows)
    W = len(rows[0]) if rows else 0
    ink = lambda x, y: 0 <= y < H and 0 <= x < W and rows[y][x]
    edges = {}
    def add(a, b):
        edges.setdefault(a, []).append(b)
    for y in range(H):
        for x in range(W):
            if not rows[y][x]:
                continue
            X0, X1 = x + cell.lsb, x + cell.lsb + 1
            T, B = asc - y, asc - y - 1          # y-up pixel coordinates
            if not ink(x, y - 1): add((X0, T), (X1, T))
            if not ink(x + 1, y): add((X1, T), (X1, B))
            if not ink(x, y + 1): add((X1, B), (X0, B))
            if not ink(x - 1, y): add((X0, B), (X0, T))
    pen = TTGlyphPen(None)
    used = set()
    def direction(a, b):
        return (b[0] - a[0], b[1] - a[1])
    while True:
        start = None
        for a, outs in edges.items():
            for b in outs:
                if (a, b) not in used:
                    start = (a, b); break
            if start: break
        if not start:
            break
        loop = [start[0]]
        a, b = start
        used.add((a, b))
        while True:
            loop.append(b)
            if b == loop[0]:
                break
            d = direction(a, b)
            cands = [c for c in edges.get(b, []) if (b, c) not in used]
            if len(cands) > 1:
                # prefer a right turn (keeps diagonal-touching pixels separate)
                right = (d[1], -d[0])
                cands.sort(key=lambda c: 0 if direction(b, c) == right else 1)
            c = cands[0]
            used.add((b, c))
            a, b = b, c
        pts = loop[:-1]
        # drop collinear points
        simp = []
        n = len(pts)
        for i in range(n):
            p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
            if (p1[0] - p0[0]) * (p2[1] - p1[1]) - (p1[1] - p0[1]) * (p2[0] - p1[0]) != 0:
                simp.append(p1)
        pen.moveTo((simp[0][0] * unit, simp[0][1] * unit))
        for p in simp[1:]:
            pen.lineTo((p[0] * unit, p[1] * unit))
        pen.closePath()
    return pen.glyph()

# ------------------------------------------------------- EBLC / EBDT
def crop(cell):
    rows = cell.rows
    H = len(rows)
    W = len(rows[0]) if rows else 0
    ys = [y for y in range(H) if any(rows[y])]
    if not ys or W == 0:
        return None
    xs = [x for x in range(W) if any(rows[y][x] for y in range(H))]
    y0, y1, x0, x1 = ys[0], ys[-1], xs[0], xs[-1]
    bmp = [r[x0:x1 + 1] for r in rows[y0:y1 + 1]]
    return bmp, x0 + cell.lsb, y0

def build_strikes(order, strikes):
    """strikes: list of (ppem, asc, dsc, {glyphname: Cell}). Returns (EBLC bytes, EBDT bytes)."""
    ebdt = bytearray(struct.pack('>HH', 2, 0))
    size_records = []
    sub_blobs = []
    for ppem, asc, dsc, cmap in strikes:
        img_start = len(ebdt)
        offsets = []
        first, last = 1, len(order) - 1
        gids = range(first, last + 1)
        m_bx, m_adv_sb, m_before, m_after, wmax = 127, 127, -128, 127, 0
        for gid in gids:
            offsets.append(len(ebdt) - img_start)
            cell = cmap.get(order[gid])
            if cell is None:
                continue
            c = crop(cell)
            if c is None:
                bmp, bx, top = [[0]], 0, asc - 1
            else:
                bmp, bx, top = c
            h, w = len(bmp), len(bmp[0])
            by = asc - top
            adv = cell.adv
            ebdt += struct.pack('>BBbbB', h, w, bx, by, adv)
            for r in bmp:
                bits = 0
                nbytes = (w + 7) // 8
                for i, v in enumerate(r):
                    if v:
                        bits |= 1 << (nbytes * 8 - 1 - i)
                ebdt += bits.to_bytes(nbytes, 'big')
            if c is not None:
                m_bx = min(m_bx, bx)
                m_adv_sb = min(m_adv_sb, adv - (bx + w))
                m_before = max(m_before, by)
                m_after = min(m_after, by - h)
            wmax = max(wmax, adv, w)
        offsets.append(len(ebdt) - img_start)
        # index subtable format 1, image format 1
        sub = struct.pack('>HHI', 1, 1, img_start) + b''.join(struct.pack('>I', o) for o in offsets)
        arr = struct.pack('>HHI', first, last, 8)   # one entry, subtable follows the 8-byte array
        sub_blobs.append(arr + sub)
        line = struct.pack('>bbBbbbbbbbbb', asc, -dsc, wmax, 1, 0, 0,
                           m_bx, m_adv_sb, m_before, m_after, 0, 0)
        size_records.append((len(arr + sub), line, first, last, ppem))
    header = struct.pack('>HHI', 2, 0, len(strikes))
    off = len(header) + 48 * len(strikes)
    recs = bytearray()
    blobs = bytearray()
    for (size, line, first, last, ppem), blob in zip(size_records, sub_blobs):
        recs += struct.pack('>IIII', off + len(blobs), size, 1, 0)
        recs += line + line
        recs += struct.pack('>HHBBBb', first, last, ppem, ppem, 1, 1)
        blobs += blob
        while len(blobs) % 4:
            blobs += b'\0'
    return bytes(header + recs + blobs), bytes(ebdt)

# ------------------------------------------------------------ TTF
def make_ttf(path, family, style, weight_cells, outline_ppem, strike_ppems, upm_ppem):
    """weight_cells: {ppem: {char: Cell}}"""
    chars = charset({p: weight_cells[p] for p in strike_ppems})
    order = ['.notdef'] + [gname(c) for c in chars]
    assert len(set(order)) == len(order)
    _, oasc, odsc = swarf.SIZES[outline_ppem]
    m = swarf.SIZES[outline_ppem][0]
    unit = PX * upm_ppem // outline_ppem
    upm = PX * upm_ppem
    ocells = dict(weight_cells[outline_ppem])
    ocells['.notdef'] = notdef_cell(ocells, outline_ppem)
    glyphs, metrics = {}, {}
    for ch in ['.notdef'] + chars:
        c = ocells[ch]
        g = outline_glyph(c, oasc, unit)
        n = gname(ch)
        glyphs[n] = g
        metrics[n] = (c.adv * unit, c.lsb * unit)
    fb = FontBuilder(upm, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({ord(c): gname(c) for c in chars})
    fb.setupGlyf(glyphs)
    # fix lsb to real bbox
    glyf = fb.font['glyf']
    hm = {}
    for n in order:
        g = glyf[n]
        g.recalcBounds(glyf)
        lsb = getattr(g, 'xMin', 0) if g.numberOfContours else 0
        hm[n] = (metrics[n][0], lsb)
    fb.setupHorizontalMetrics(hm)
    asc_u, dsc_u = oasc * unit, odsc * unit
    fb.setupHorizontalHeader(ascent=asc_u, descent=-dsc_u, lineGap=0)
    full = family if style == 'Regular' else f'{family} {style}'
    ps = f"{family.replace(' ', '')}-{style}"
    fb.setupNameTable({
        'copyright': COPYRIGHT,
        'familyName': family,
        'styleName': style,
        'uniqueFontIdentifier': f'{VERSION};{VENDOR};{ps}',
        'fullName': full,
        'version': f'Version {VERSION}',
        'psName': ps,
        'manufacturer': 'techrote',
        'designer': 'techrote + Claude',
        'description': 'BLUED SWARF — a hand-tuned multi-size pixel font in the spirit of DOS / Windows 3.x system fonts. '
                       'Pixel-exact at 6-16px.',
    })
    master = swarf.MASTER_SPECS[m]
    bold = style == 'Bold'
    fb.setupOS2(
        usWeightClass=700 if bold else 400,
        usWidthClass=5,
        fsType=0,
        achVendID=VENDOR,
        fsSelection=(0x20 if bold else 0x40) | 0x80,
        sTypoAscender=asc_u, sTypoDescender=-dsc_u, sTypoLineGap=0,
        usWinAscent=asc_u, usWinDescent=dsc_u,
        sxHeight=master['x'] * unit, sCapHeight=master['cap'] * unit,
        ySubscriptXSize=upm // 2, ySubscriptYSize=upm // 2, ySubscriptYOffset=upm // 8,
        ySuperscriptXSize=upm // 2, ySuperscriptYSize=upm // 2, ySuperscriptYOffset=upm // 3,
        yStrikeoutSize=unit, yStrikeoutPosition=(master['x'] // 2) * unit,
        version=4,
    )
    os2 = fb.font['OS/2']
    from fontTools.ttLib.tables.O_S_2f_2 import Panose
    os2.panose = Panose()
    os2.panose.bFamilyType = 2
    os2.panose.bSerifStyle = 11      # normal sans
    os2.panose.bWeight = 8 if bold else 5
    os2.panose.bProportion = 3
    os2.recalcUnicodeRanges(fb.font)
    os2.recalcCodePageRanges(fb.font)
    fb.setupPost(underlinePosition=-unit, underlineThickness=unit, isFixedPitch=0)
    head = fb.font['head']
    head.flags |= (1 << 4) | (1 << 3)     # non-linear advances (hdmx), integer ppem
    head.fontRevision = float(VERSION)
    head.macStyle = 1 if bold else 0
    now = int((datetime.datetime(2026, 10, 12) - datetime.datetime(1904, 1, 1)).total_seconds())
    head.created = head.modified = now
    # gasp: no grid-fitting, no smoothing — pixel edges stay hard
    gasp = newTable('gasp')
    gasp.version = 1
    gasp.gaspRange = {0xFFFF: 0x0000}
    fb.font['gasp'] = gasp
    # embedded bitmap strikes
    strikes = []
    hdmx = {}
    for p in strike_ppems:
        _, a, d = swarf.SIZES[p]
        cells = dict(weight_cells[p])
        cells['.notdef'] = notdef_cell(cells, p)
        cmap = {gname(ch): c for ch, c in cells.items() if gname(ch) in set(order)}
        strikes.append((p, a, d, cmap))
        hdmx[p] = {n: cmap[n].adv for n in order}
    eblc, ebdt = build_strikes(order, strikes)
    t = DefaultTable('EBDT'); t.data = ebdt; fb.font['EBDT'] = t
    t = DefaultTable('EBLC'); t.data = eblc; fb.font['EBLC'] = t
    hd = newTable('hdmx')
    hd.version = 0
    hd.hdmx = hdmx
    fb.font['hdmx'] = hd
    fb.font['maxp'].maxPoints = max(fb.font['maxp'].maxPoints, 0)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fb.save(path)
    return fb.font

# ------------------------------------------------------------ FNT / FON
CP1252 = [bytes([b]).decode('cp1252', errors='replace') for b in range(256)]

def make_fnt(cells, ppem, face, bold):
    _, asc, dsc = swarf.SIZES[ppem]
    H = asc + dsc
    first, last = 0x20, 0xFF
    default = cells['?']
    entries = []
    for b in range(first, last + 1):
        ch = CP1252[b]
        c = cells.get(ch)
        if c is None or ch == '�':
            c = default
        entries.append(c)
    entries.append(cells[' '])                 # sentinel "absolute space"
    header_size = 118
    table_size = 4 * len(entries)
    bits_off = header_size + table_size
    bitmaps = bytearray()
    table = bytearray()
    for c in entries:
        w = c.adv
        table += struct.pack('<HH', w, bits_off + len(bitmaps))
        strips = (w + 7) // 8
        rows = c.rows
        for s in range(strips):
            for y in range(H):
                byte = 0
                for k in range(8):
                    x = s * 8 + k - c.lsb
                    if 0 <= x < (len(rows[y]) if rows[y] else 0) and rows[y][x]:
                        byte |= 0x80 >> k
                bitmaps.append(byte)
    face_off = bits_off + len(bitmaps)
    face_b = face.encode('ascii') + b'\0'
    total = face_off + len(face_b)
    widths = [c.adv for c in entries[:-1]]
    avg = cells['x'].adv
    copyright_b = COPYRIGHT.encode('ascii')[:59].ljust(60, b'\0')
    points = max(1, round(ppem * 72 / 96))
    wbytes = sum((c.adv + 7) // 8 for c in entries[:-1])
    wbytes += wbytes % 2
    hdr = struct.pack('<HI60sHHHHHHHBBBHBHHBHHBBBBHIIII',
                      0x0200, total, copyright_b, 0, points, 96, 96,
                      asc, 0, 0, 0, 0, 0, 700 if bold else 400, 0,
                      0, H, 0x21,   # pixwidth 0 = variable; FF_SWISS | variable pitch bit
                      avg, max(widths), first, last,
                      ord('?') - first, ord(' ') - first, wbytes, 0, face_off, 0, bits_off)
    hdr += b'\0'                                  # dfReserved
    assert len(hdr) == header_size, len(hdr)
    return bytes(hdr + table + bitmaps + face_b)

def make_fon(path, fnts, face, module):
    """Wrap FNT resources into a 16-bit NE font library (.fon)."""
    # FONTDIR
    fontdir = struct.pack('<H', len(fnts))
    for i, f in enumerate(fnts):
        fontdir += struct.pack('<H', i + 1) + f[:0x71] + b'\0' + face.encode('ascii') + b'\0'
    # DOS stub
    stub_code = bytes([0x0e, 0x1f, 0xba, 0x0e, 0x00, 0xb4, 0x09, 0xcd, 0x21,
                       0xb8, 0x01, 0x4c, 0xcd, 0x21])
    stub_msg = b'This is a Windows font file.\r\n$'
    stub = stub_code + stub_msg
    stub += b'\0' * (-len(stub) % 16)
    ne_off = 0x40 + len(stub)
    ne_off += -ne_off % 16
    total_stub = ne_off
    mz = bytearray(0x40)
    struct.pack_into('<2sHHHHHHHHHHHHH', mz, 0, b'MZ', total_stub % 512, (total_stub + 511) // 512,
                     0, 4, 0x10, 0xFFFF, 0, 0xB8, 0, 0, 0, 0x40, 0)
    struct.pack_into('<I', mz, 0x3C, ne_off)
    dos = bytes(mz) + stub
    dos += b'\0' * (ne_off - len(dos))

    align = 4
    # resource table (built twice: once to size, once with offsets)
    def restable(offsets):
        rt = struct.pack('<H', align)
        rt += struct.pack('<HHI', 0x8007, 1, 0)
        o, l = offsets[0]
        name_off = 2 + 8 + 12 + 8 + 12 * len(fnts) + 2
        rt += struct.pack('<HHHHI', o, l, 0x0c50, name_off, 0)   # FONTDIR, named "FONTDIR"
        rt += struct.pack('<HHI', 0x8008, len(fnts), 0)
        for i in range(len(fnts)):
            o, l = offsets[i + 1]
            rt += struct.pack('<HHHHI', o, l, 0x1c30, 0x8001 + i, 0)
        rt += struct.pack('<H', 0)
        rt += b'\x07FONTDIR' + b'\0'
        return rt
    res_tab = restable([(0, 0)] * (len(fnts) + 1))
    modname = module.upper().encode('ascii')
    resident = bytes([len(modname)]) + modname + struct.pack('<H', 0) + b'\0'
    modref = b''
    imported = b'\0'
    entry = b'\0\0'
    desc = f'FONTRES 100,96,96 : {face}'.encode('ascii')
    nonresident = bytes([len(desc)]) + desc + struct.pack('<H', 0) + b'\0'

    ne_len = 0x40
    res_off = ne_len
    resid_off = res_off + len(res_tab)
    modref_off = resid_off + len(resident)
    imp_off = modref_off + len(modref)
    entry_off = imp_off + len(imported)
    nonres_off_abs = ne_off + entry_off + len(entry)
    after = nonres_off_abs + len(nonresident)
    # resource data, aligned
    datas = [fontdir] + list(fnts)
    offsets = []
    pos = after
    pos += -pos % (1 << align)
    layout = []
    for d in datas:
        offsets.append((pos >> align, (len(d) + (1 << align) - 1) >> align))
        layout.append((pos, d))
        pos += len(d)
        pos += -pos % (1 << align)
    res_tab = restable(offsets)
    assert len(res_tab) == resid_off - res_off

    ne = bytearray(0x40)
    struct.pack_into('<2sBBHH', ne, 0, b'NE', 5, 10, entry_off, len(entry))
    struct.pack_into('<I', ne, 0x08, 0)
    struct.pack_into('<H', ne, 0x0C, 0x8300)
    struct.pack_into('<HHHII', ne, 0x0E, 0, 0, 0, 0, 0)
    struct.pack_into('<HHH', ne, 0x1C, 0, 0, len(nonresident))
    struct.pack_into('<HHHHH', ne, 0x22, ne_len, res_off, resid_off, modref_off, imp_off)
    struct.pack_into('<I', ne, 0x2C, nonres_off_abs)
    struct.pack_into('<HHH', ne, 0x30, 0, align, 0)
    struct.pack_into('<BB', ne, 0x36, 2, 0)
    struct.pack_into('<HHHH', ne, 0x38, 0, 0, 0, 0x0300)
    blob = bytearray(dos) + ne + res_tab + resident + modref + imported + entry + nonresident
    assert len(blob) == after, (len(blob), after)
    for p, d in layout:
        blob += b'\0' * (p - len(blob))
        blob += d
    blob += b'\0' * (-len(blob) % (1 << align))
    with open(path, 'wb') as f:
        f.write(blob)

# ------------------------------------------------------------ BDF
def make_bdf(path, cells, ppem, family, bold):
    _, asc, dsc = swarf.SIZES[ppem]
    chars = sorted(cells, key=ord)
    lines = ['STARTFONT 2.1',
             f'FONT -techrote-{family.replace(" ", "")}-{"Bold" if bold else "Medium"}-R-Normal--{ppem}-{ppem*10}-96-96-P-{cells["x"].adv*10}-ISO10646-1',
             f'SIZE {ppem} 96 96',
             f'FONTBOUNDINGBOX {max(c.adv for c in cells.values())} {asc+dsc} 0 {-dsc}',
             'STARTPROPERTIES 8',
             f'FAMILY_NAME "{family}"', f'WEIGHT_NAME "{"Bold" if bold else "Medium"}"',
             f'PIXEL_SIZE {ppem}', f'FONT_ASCENT {asc}', f'FONT_DESCENT {dsc}',
             'DEFAULT_CHAR 63', f'COPYRIGHT "{COPYRIGHT}"', 'SPACING "P"',
             'ENDPROPERTIES', f'CHARS {len(chars)}']
    for ch in chars:
        c = cells[ch]
        cr = crop(c)
        if cr is None:
            bmp, bx, top = [], 0, asc
            h, w = 0, 0
        else:
            bmp, bx, top = cr
            h, w = len(bmp), len(bmp[0])
        lines += [f'STARTCHAR {gname(ch)}', f'ENCODING {ord(ch)}',
                  f'SWIDTH {round(c.adv * 1000 / ppem)} 0', f'DWIDTH {c.adv} 0',
                  f'BBX {w} {h} {bx} {asc - top - h if h else 0}', 'BITMAP']
        for r in bmp:
            nb = (w + 7) // 8
            v = 0
            for i, b in enumerate(r):
                if b:
                    v |= 1 << (nb * 8 - 1 - i)
            lines.append(f'{v:0{nb*2}X}')
        lines.append('ENDCHAR')
    lines.append('ENDFONT')
    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')

# ------------------------------------------------------------ main
def main():
    ms, reg, bold = swarf.all_sizes()
    sizes = sorted(swarf.SIZES)
    os.makedirs(OUT, exist_ok=True)
    built = []
    for style, cells in (('Regular', reg), ('Bold', bold)):
        isb = style == 'Bold'
        # universal
        p = os.path.join(OUT, f'{STEM}-{style}.ttf')
        make_ttf(p, FAMILY, style, cells, DESIGN_PPEM, sizes, DESIGN_PPEM)
        built.append(p)
        for n in sizes:
            fam = f'{FAMILY} {n}px'
            p = os.path.join(OUT, 'per-size', f'{STEM}{n}px-{style}.ttf')
            font = make_ttf(p, fam, style, cells, n, [n], n)
            built.append(p)
            os.makedirs(os.path.join(OUT, 'web'), exist_ok=True)
            font.flavor = 'woff2'
            w = os.path.join(OUT, 'web', f'{STEM}{n}px-{style}.woff2')
            font.save(w)
            os.makedirs(os.path.join(OUT, 'bdf'), exist_ok=True)
            make_bdf(os.path.join(OUT, 'bdf', f'{STEM}-{n}px-{style}.bdf'), cells[n], n, FAMILY, isb)
        os.makedirs(os.path.join(OUT, 'windows-fon'), exist_ok=True)
        face = FON_FACE
        fnts = [make_fnt(cells[n], n, face, isb) for n in sizes]
        fp = os.path.join(OUT, 'windows-fon', FON_FILES[isb])
        make_fon(fp, fnts, face, 'BLUEDSYS' if not isb else 'BLUEDSYB')
        built.append(fp)
    for b in built:
        print(os.path.relpath(b, OUT), os.path.getsize(b))

if __name__ == '__main__':
    main()
