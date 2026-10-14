#!/usr/bin/env python3
"""Render a PNG proof sheet of the Fourth Cohort TTFs with FreeType (no PIL needed).
Copyright (c) 2026 techrote. SIL Open Font License 1.1.

  python tools/fourth_cohort/render.py [OUT.png] [--size 56] [--glyphs]
--glyphs renders every ASCII character large, one font per sheet suffix, for review.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import struct
import zlib

import freetype

ROOT = Path(__file__).resolve().parents[2]
FONTS = (
    ('Gasket Sans', 'cmd-font-container/gasket-sans/fonts/GasketSans-Regular.ttf'),
    ('Ratchet Block', 'hot-font-box/ratchet-block/fonts/RatchetBlock-Regular.ttf'),
    ('Phase Drift', 'cachemonic/phase-drift/fonts/PhaseDrift-Regular.ttf'),
)
LINES = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz',
         '0123456789 !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
PAPER = 247


def draw_line(img, w, h, face, text, x, baseline, wrap=None):
    for ch in text:
        face.load_char(ch, freetype.FT_LOAD_RENDER)
        bm, left, top = face.glyph.bitmap, face.glyph.bitmap_left, face.glyph.bitmap_top
        for r in range(bm.rows):
            yy = baseline - top + r
            if not 0 <= yy < h:
                continue
            row = img[yy]
            for c in range(bm.width):
                xx = x + left + c
                if 0 <= xx < w:
                    v = PAPER - bm.buffer[r * bm.pitch + c] * PAPER // 255
                    if v < row[xx]:
                        row[xx] = v
        x += face.glyph.advance.x >> 6
        if wrap and x > wrap:
            break
    return x


def write_png(path, img, w, h):
    raw = b''.join(b'\x00' + bytes(row) for row in img)
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 0, 0, 0, 0))
                     + chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b''))


def sheet(out, size):
    w = 1500
    title = size * 2
    faces = []
    for name, rel in FONTS:
        f = freetype.Face(str(ROOT / rel))
        faces.append((name, f))
    block = int(title * 1.1 + len(LINES) * size * 1.7 + size)
    h = block * len(faces) + 40
    img = [[PAPER] * w for _ in range(h)]
    y = 20
    for name, face in faces:
        face.set_char_size(title * 64)
        draw_line(img, w, h, face, name, 24, y + int(title * 0.85))
        face.set_char_size(size * 64)
        base = y + int(title * 1.1) + int(size * 1.1)
        for line in LINES:
            draw_line(img, w, h, face, line, 24, base, wrap=w - 40)
            base += int(size * 1.7)
        y += block
    write_png(out, img, w, h)


def glyph_sheet(out, size=110):
    """Every ASCII glyph at a large size; three sheets, one per family."""
    chars = [chr(i) for i in range(33, 127)]
    cols = 12
    cell = int(size * 1.25)
    for name, rel in FONTS:
        face = freetype.Face(str(ROOT / rel))
        face.set_char_size(size * 64)
        rows = (len(chars) + cols - 1) // cols
        w, h = cols * cell + 20, rows * cell + 20
        img = [[PAPER] * w for _ in range(h)]
        for i, ch in enumerate(chars):
            draw_line(img, w, h, face, ch, 10 + (i % cols) * cell + cell // 8,
                      10 + (i // cols) * cell + int(size * 0.95))
        write_png(out.with_name(out.stem + '-' + name.lower().replace(' ', '-') + '.png'), img, w, h)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('out', nargs='?', type=Path, default=ROOT / 'docs' / 'fourth-cohort-render.png')
    p.add_argument('--size', type=int, default=56)
    p.add_argument('--glyphs', action='store_true')
    a = p.parse_args()
    (glyph_sheet if a.glyphs else lambda o, s=None: sheet(o, a.size))(a.out.resolve())
    print('wrote', a.out)
