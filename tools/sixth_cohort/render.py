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

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('out', nargs='?', type=Path, default=base.ROOT / 'docs' / 'sixth-cohort-render.png')
    p.add_argument('--size', type=int, default=44)
    a = p.parse_args()
    base.sheet(a.out.resolve(), a.size)
    print('wrote', a.out)
