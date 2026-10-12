"""Round-trip check: render every glyph of every output with FreeType and compare
with the engine's source bitmaps (pixel-exact, including bearings and advances)."""
import os, sys, glob
import freetype
from fontTools.ttLib import TTFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import swarf, build

OUT = build.OUT
GREY = []

def ft_bitmap(face, ch, flags):
    face.load_char(ch, flags)
    g = face.glyph
    bm = g.bitmap
    rows = []
    for y in range(bm.rows):
        row = []
        for x in range(bm.width):
            if bm.pixel_mode == freetype.FT_PIXEL_MODE_MONO:
                byte = bm.buffer[y * bm.pitch + x // 8]
                row.append(1 if byte & (0x80 >> (x % 8)) else 0)
            else:
                v = bm.buffer[y * bm.pitch + x]
                if v not in (0, 255):
                    GREY.append(v)
                row.append(1 if v >= 128 else 0)
        rows.append(row)
    return rows, g.bitmap_left, g.bitmap_top, g.advance.x / 64.0

def expected(cell, asc):
    c = build.crop(cell)
    if c is None:
        return [], None, None, cell.adv
    bmp, bx, top = c
    return bmp, bx, asc - top, cell.adv

def trim(rows, left, top):
    """Normalise a FreeType bitmap to its ink bbox."""
    ys = [y for y, r in enumerate(rows) if any(r)]
    if not ys:
        return [], None, None
    xs = [x for x in range(len(rows[0])) if any(r[x] for r in rows)]
    return [r[xs[0]:xs[-1] + 1] for r in rows[ys[0]:ys[-1] + 1]], left + xs[0], top - ys[0]

def check(face, cells, ppem, flags, label, adv_tol=0.0, keymap=None):
    _, asc, dsc = swarf.SIZES[ppem]
    bad = []
    for ch, cell in cells.items():
        exp = expected(cell, asc)
        key = keymap[ch] if keymap else ch
        if face.get_char_index(key) == 0:
            bad.append((ch, 'missing')); continue
        rows, left, top, adv = ft_bitmap(face, key, flags)
        got = trim(rows, left, top)
        if False:
            bad.append((ch, 'missing')); continue
        if (got[0], got[1], got[2]) != (exp[0], exp[1], exp[2]) or abs(adv - exp[3]) > adv_tol:
            bad.append((ch, f'got {got[1:]} adv {adv} vs {exp[1:3]} adv {exp[3]}'))
    status = 'OK ' if not bad else 'BAD'
    print(f'{status} {label:40s} {len(cells)} glyphs' + (f'  {len(bad)} mismatches e.g. {bad[:3]}' if bad else ''))
    return not bad

def main():
    ms, reg, bold = swarf.all_sizes()
    ok = True
    for style, cells in (('Regular', reg), ('Bold', bold)):
        # universal: embedded bitmaps
        path = os.path.join(OUT, f'{build.STEM}-{style}.ttf')
        TTFont(path)['EBLC'].strikes  # fontTools can parse our tables
        face = freetype.Face(path)
        for p in sorted(swarf.SIZES):
            face.set_pixel_sizes(0, p)
            ok &= check(face, cells[p], p, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO,
                        f'{style} universal strike {p}px')
        # universal outline at 10/20px
        face.set_pixel_sizes(0, 10)
        ok &= check(face, cells[10], 10, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_BITMAP |
                    freetype.FT_LOAD_NO_HINTING | freetype.FT_LOAD_TARGET_MONO, f'{style} universal outline 10px')
        # per-size: outlines only (no bitmap) must be pixel exact too
        for p in sorted(swarf.SIZES):
            path = os.path.join(OUT, 'per-size', f'{build.STEM}{p}px-{style}.ttf')
            face = freetype.Face(path)
            face.set_pixel_sizes(0, p)
            ok &= check(face, cells[p], p, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_BITMAP |
                        freetype.FT_LOAD_NO_HINTING | freetype.FT_LOAD_TARGET_MONO, f'{style} per-size outline {p}px')
            ok &= check(face, cells[p], p, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING,
                        f'{style} per-size AA outline {p}px')
            ok &= check(face, cells[p], p, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO,
                        f'{style} per-size strike {p}px')
        # FON: one face per size, cp1252 only
        fon = os.path.join(OUT, 'windows-fon', build.FON_FILES[style == 'Bold'])
        n = freetype.Face(fon).num_faces
        assert n == len(swarf.SIZES), n
        for i, p in enumerate(sorted(swarf.SIZES)):
            face = freetype.Face(fon, i)
            assert face.available_sizes[0].height == p, (face.available_sizes[0].height, p)
            face.select_size(0)
            face.set_charmap(face.charmaps[0])
            sub, km = {}, {}
            for b in range(0x20, 0x100):
                ch = bytes([b]).decode('cp1252', errors='replace')
                if ch in cells[p] and ch != '�':
                    sub[ch] = cells[p][ch]; km[ch] = b
            ok &= check(face, sub, p, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO,
                        f'{style} FON {p}px ({face.family_name.decode()})', keymap=km)
    print('grey (partial) pixels seen in AA renders:', len(GREY))
    print('ALL OK' if ok and not GREY else 'FAILURES')

if __name__ == '__main__':
    main()
