#!/usr/bin/env python3
"""Render the Sixth Cohort proof sheet (reuses the Fourth Cohort FreeType renderer).
  python tools/sixth_cohort/render.py [OUT.png] [--size 44]
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
"""
import argparse
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'fourth_cohort'))
import render as base  # noqa: E402

base.FONTS = (
    ('Lathe Round', 'cmd-font-container/lathe-round/fonts/LatheRound-Regular.ttf'),
    ('Rivet Condensed', 'cmd-font-container/rivet-condensed/fonts/RivetCondensed-Regular.ttf'),
    ('Spindle Stencil', 'hot-font-box/spindle-stencil/fonts/SpindleStencil-Regular.ttf'),
    ('Cleat Inline', 'hot-font-box/cleat-inline/fonts/CleatInline-Regular.ttf'),
    ('Slip Echo', 'cachemonic/slip-echo/fonts/SlipEcho-Regular.ttf'),
    ('Fault Line', 'cachemonic/fault-line/fonts/FaultLine-Regular.ttf'),
)
EXTRA = tuple((n, f"{p}/{n.lower().replace(' ', '-')}/fonts/{n.replace(' ', '')}-Regular.ttf") for n, p in (
    ('Skiff Slant', 'cmd-font-container'), ('Pebble Bold', 'cmd-font-container'),
    ('Gantry Light', 'cmd-font-container'), ('Girder Mono', 'cmd-font-container'),
    ('Bobbin Outline', 'hot-font-box'), ('Ingot Shadow', 'hot-font-box'), ('Slab Brick', 'hot-font-box'),
    ('Raster Slit', 'cachemonic'), ('Band Slip', 'cachemonic'), ('Punch Card', 'cachemonic'),
    ('Quantum Step', 'cachemonic'), ('Hatch Block', 'cachemonic')))
MORE = tuple((n, f"{p}/{n.lower().replace(' ', '-')}/fonts/{n.replace(' ', '')}-Regular.ttf") for n, p in (
    ('Ferrule Regular', 'cmd-font-container'), ('Tallow Condensed', 'cmd-font-container'),
    ('Pillow Block', 'hot-font-box'), ('Contour Ripple', 'hot-font-box'),
    ('Comb Cut', 'cachemonic'), ('Wave Warp', 'cachemonic')))

LAST = tuple((n, f"{p}/{n.lower().replace(' ', '-')}/fonts/{n.replace(' ', '')}-Regular.ttf") for n, p in (
    ('Plinth Slab', 'cmd-font-container'), ('Plinth Mono', 'cmd-font-container'),
    ('Stride Wide', 'cmd-font-container'), ('Tendon Backslant', 'cmd-font-container'),
    ('Anvil Slab', 'hot-font-box'), ('Anvil Twin', 'hot-font-box'),
    ('Cantilever Shadow', 'hot-font-box'), ('Girth Block', 'hot-font-box'),
    ('Gravel Grit', 'cachemonic'), ('Misprint Duo', 'cachemonic'),
    ('Saw Warp', 'cachemonic'), ('Pixel Cell', 'cachemonic')))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('out', nargs='?', type=Path, default=None)
    p.add_argument('--size', type=int, default=44)
    p.add_argument('--extra', action='store_true', help='render the twelve later additions')
    p.add_argument('--more', action='store_true', help='render the six latest additions')
    p.add_argument('--last', action='store_true', help='render the twelve latest additions')
    a = p.parse_args()
    if a.last:
        base.FONTS = LAST
    if a.extra:
        base.FONTS = EXTRA
    if a.more:
        base.FONTS = MORE
    a.out = a.out or base.ROOT / 'docs' / ('sixth-cohort-render-4.png' if a.last else 'sixth-cohort-render-3.png' if a.more else 'sixth-cohort-render-2.png' if a.extra else 'sixth-cohort-render.png')
    base.sheet(a.out.resolve(), a.size)
    print('wrote', a.out)
