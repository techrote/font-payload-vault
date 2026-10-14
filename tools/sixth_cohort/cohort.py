#!/usr/bin/env python3
"""Sixth Cohort: build six families (three lineages, many treatments) and proofs.

Reuses the Fourth Cohort build/proof code and the Original Trio serializer.
Run from the repository root:  python tools/sixth_cohort/cohort.py
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'tools' / 'fourth_cohort'))

import cohort as base  # noqa: E402  (fourth_cohort/cohort.py, shared build and proofs)

base.FAMILIES = (
    'cmd-font-container/lathe-round',
    'cmd-font-container/rivet-condensed',
    'hot-font-box/spindle-stencil',
    'hot-font-box/cleat-inline',
    'cachemonic/slip-echo',
    'cachemonic/fault-line',
    'cmd-font-container/skiff-slant',
    'cmd-font-container/pebble-bold',
    'cmd-font-container/gantry-light',
    'cmd-font-container/girder-mono',
    'hot-font-box/bobbin-outline',
    'hot-font-box/ingot-shadow',
    'hot-font-box/slab-brick',
    'cachemonic/raster-slit',
    'cachemonic/band-slip',
    'cachemonic/punch-card',
    'cachemonic/quantum-step',
    'cachemonic/hatch-block',
    'cmd-font-container/ferrule-regular',
    'cmd-font-container/tallow-condensed',
    'hot-font-box/pillow-block',
    'hot-font-box/contour-ripple',
    'cachemonic/comb-cut',
    'cachemonic/wave-warp',
)
base.VERSION = '1.000'
base.trio.VERSION = base.VERSION
base.COHORT = 'SIXTH COHORT 06'
base.MANIFEST = 'sixth-cohort-manifest.json'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT)
    parser.add_argument('--proofs-only', action='store_true')
    args = parser.parse_args()
    out = args.output.resolve()
    if not args.proofs_only:
        base.build_fonts(out)
    base.build_proofs(out)
