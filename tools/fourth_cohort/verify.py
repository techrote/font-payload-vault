#!/usr/bin/env python3
"""Verify the Fourth or Sixth Cohort fonts with the Original Trio test methods.

  python tools/fourth_cohort/verify.py --cohort sixth --require-ots [--report FILE]

Ports the family-independent Original Trio checks (exact repertoire, outline match
against the quantized master, metrics and bounds, names, FreeType TTF-vs-WOFF2 raster
parity, OTS, separate-process reproducibility). The Latchline- and Diecast-specific
tests are not applicable. Siblings on a shared skeleton are not required to differ.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
"""
from __future__ import annotations
import argparse
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools' / 'sixth_cohort'))
sys.path.insert(0, str(ROOT / 'tools' / 'original_trio'))

import freetype  # noqa: E402
from fontTools.ttLib import TTFont  # noqa: E402
from geometry import contours  # noqa: E402
from repertoire import COVERAGE, BLANKS  # noqa: E402
from build import TIMESTAMP, glyph_name  # noqa: E402

COHORT = None
REQUIRE_OTS = False
MODULE = None


def load_cohort(name):
    path = ROOT / 'tools' / ('fourth_cohort' if name == 'fourth' else 'sixth_cohort') / 'cohort.py'
    spec = importlib.util.spec_from_file_location(f'cohort_{name}', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.base if name == 'sixth' else mod


def outline(font, c):
    glyph = font['glyf'][glyph_name(c)]
    if glyph.numberOfContours == 0:
        return []
    coords, ends, _ = glyph.getCoordinates(font['glyf'])
    result, start = [], 0
    for end in ends:
        pts = [tuple(p) for p in coords[start:end + 1]]
        pivot = min(range(len(pts)), key=lambda i: pts[i:] + pts[:i])
        result.append(pts[pivot:] + pts[:pivot])
        start = end + 1
    return sorted(result)


def raster(face, c, px):
    face.set_pixel_sizes(0, px)
    face.load_char(c, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING)
    slot = face.glyph
    b = slot.bitmap
    return (slot.bitmap_left, slot.bitmap_top, b.width, b.rows, b.pitch, bytes(b.buffer))


class FontTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = []
        for relative in MODULE.FAMILIES:
            mod, shapes = MODULE.shapes_for(ROOT / relative)
            stem = mod.FAMILY.replace(' ', '') + '-Regular'
            paths = [ROOT / relative / 'fonts' / (stem + '.' + ext) for ext in ('ttf', 'woff2')]
            cls.entries.append((mod, shapes, paths))

    def test_exact_repertoire_and_nonempty(self):
        for mod, shapes, paths in self.entries:
            for p in paths:
                with self.subTest(font=p.name), TTFont(p) as font:
                    self.assertEqual(set(font.getBestCmap()), {ord(c) for c in COVERAGE})
                    self.assertEqual(font['maxp'].numGlyphs, len(COVERAGE) + 1)
                    self.assertGreater(font['glyf']['.notdef'].numberOfContours, 0)
                    for c in COVERAGE:
                        self.assertEqual(font['glyf'][glyph_name(c)].numberOfContours == 0, c in BLANKS, (p.name, c))

    def test_outlines_match_quantized_master(self):
        for mod, shapes, paths in self.entries:
            for p in paths:
                with self.subTest(font=p.name), TTFont(p) as font:
                    for c, (g, _) in shapes.items():
                        self.assertTrue(g.is_valid, (mod.FAMILY, c))
                        self.assertEqual(outline(font, c), sorted(contours(g)), (p.name, c))

    def test_metrics_and_bounds(self):
        for mod, shapes, paths in self.entries:
            with self.subTest(font=mod.FAMILY), TTFont(paths[0]) as font:
                self.assertEqual(font['head'].unitsPerEm, 1000)
                self.assertEqual(font['head'].created, TIMESTAMP)
                self.assertEqual(font['head'].modified, TIMESTAMP)
                self.assertEqual(font['OS/2'].version, 4)
                self.assertEqual(font['OS/2'].fsType, 0)
                self.assertTrue(font['OS/2'].fsSelection & 128)
                self.assertEqual(font['post'].isFixedPitch, int(mod.MONO))
                self.assertEqual((font['hhea'].ascent, font['hhea'].descent, font['hhea'].lineGap), (1000, -250, 0))
                for c, (g, a) in shapes.items():
                    aw, lsb = font['hmtx'][glyph_name(c)]
                    self.assertEqual(aw, a)
                    self.assertEqual(lsb, int(g.bounds[0]) if not g.is_empty else 0)
                    if mod.MONO:
                        self.assertEqual(aw, mod.ADVANCE, (mod.FAMILY, c))
                    if not g.is_empty:
                        x0, y0, x1, y1 = g.bounds
                        self.assertGreaterEqual(x0, 0, (mod.FAMILY, c, g.bounds))
                        self.assertLessEqual(x1, aw, (mod.FAMILY, c, g.bounds))
                        self.assertGreaterEqual(y0, -250, (mod.FAMILY, c, g.bounds))
                        self.assertLessEqual(y1, 1000, (mod.FAMILY, c, g.bounds))
                self.assertNotIn('GSUB', font)
                self.assertEqual('GPOS' in font, not mod.MONO)

    def test_names_and_unique_identities(self):
        identities = []
        for mod, _, paths in self.entries:
            with self.subTest(font=mod.FAMILY), TTFont(paths[0]) as font:
                self.assertEqual(font['name'].getDebugName(1), mod.FAMILY)
                self.assertEqual(font['name'].getDebugName(2), 'Regular')
                self.assertIn('SIL Open Font License', font['name'].getDebugName(13))
                self.assertEqual(font['name'].getDebugName(5), 'Version ' + MODULE.VERSION)
                identities.append(font['name'].getDebugName(6))
        self.assertEqual(len(set(identities)), len(self.entries))

    def test_all_exported_glyphs_render(self):
        # TTF versus decoded WOFF2 through independent FreeType at three sizes.
        for mod, shapes, paths in self.entries:
            with self.subTest(font=mod.FAMILY), tempfile.TemporaryDirectory() as tmp:
                decoded = Path(tmp) / 'decoded.ttf'
                with TTFont(paths[1]) as f:
                    f.flavor = None
                    f.save(decoded)
                faces = [freetype.Face(str(paths[0])), freetype.Face(str(decoded))]
                for px in (16, 24, 48):
                    for c in shapes:
                        a, b = (raster(face, c, px) for face in faces)
                        self.assertEqual(a, b, (mod.FAMILY, c, px))
                        if c not in BLANKS:
                            self.assertTrue(any(a[-1]), (mod.FAMILY, c, px))

    def test_independent_process_reproducibility(self):
        script = HERE / ('cohort.py' if COHORT == 'fourth' else '../sixth_cohort/cohort.py')
        with tempfile.TemporaryDirectory() as one, tempfile.TemporaryDirectory() as two:
            for out, seed in ((one, '1'), (two, '2')):
                env = dict(os.environ, PYTHONHASHSEED=seed)
                result = subprocess.run([sys.executable, str(script.resolve()), '--output', out],
                                        env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                self.assertEqual(result.returncode, 0, result.stdout)
            for mod, _, paths in self.entries:
                for p in paths:
                    rel = p.relative_to(ROOT)
                    with self.subTest(font=p.name):
                        a, b = (Path(one) / rel).read_bytes(), (Path(two) / rel).read_bytes()
                        self.assertEqual(a, b, 'differs between hash seeds: ' + p.name)
                        self.assertEqual(p.read_bytes(), a, 'stale committed output: ' + p.name)

    def test_opentype_sanitizer(self):
        executable = shutil.which('ots-sanitize')
        if not executable:
            if REQUIRE_OTS:
                self.fail('ots-sanitize is required but missing')
            self.skipTest('ots-sanitize unavailable')
        with tempfile.TemporaryDirectory() as tmp:
            for _, _, paths in self.entries:
                for p in paths:
                    with self.subTest(font=p.name):
                        result = subprocess.run([executable, str(p), str(Path(tmp) / (p.name + '.sanitized'))],
                                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                        self.assertEqual(result.returncode, 0, f'{p.name}: {result.stdout}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cohort', choices=('fourth', 'sixth'), required=True)
    parser.add_argument('--require-ots', action='store_true')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    COHORT, REQUIRE_OTS = args.cohort, args.require_ots
    MODULE = load_cohort(COHORT)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(FontTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if args.report:
        args.report.write_text(json.dumps({
            'cohort': COHORT, 'families': len(MODULE.FAMILIES), 'tests_run': result.testsRun,
            'failures': len(result.failures), 'errors': len(result.errors), 'skipped': len(result.skipped),
            'ots_required': REQUIRE_OTS,
            'versions': {p: importlib.metadata.version(p) for p in ('fonttools', 'shapely', 'Brotli', 'freetype-py')},
        }, indent=2) + '\n', encoding='utf-8')
    sys.exit(0 if result.wasSuccessful() else 1)
