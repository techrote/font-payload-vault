#!/usr/bin/env python3
"""Structural, geometric, raster and reproducibility checks for Original Trio.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import itertools
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import freetype
from fontTools.ttLib import TTFont
from geometry import contours, polygons, translate, box, merge
from repertoire import COVERAGE, BLANKS, BOX_ARMS, extend
from build import ROOT, FAMILIES, TIMESTAMP, KERN, master, glyph_name

REQUIRE_OTS = False


def outline(font,c):
    glyph=font['glyf'][glyph_name(c)]
    if glyph.numberOfContours==0: return []
    coords,ends,_=glyph.getCoordinates(font['glyf'])
    result=[];start=0
    for end in ends:
        pts=[tuple(p) for p in coords[start:end+1]]
        pivot=min(range(len(pts)),key=lambda i:pts[i:]+pts[:i])
        result.append(pts[pivot:]+pts[:pivot]);start=end+1
    return sorted(result)


def raster(face,c,px):
    face.set_pixel_sizes(0,px)
    face.load_char(c,freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING)
    slot=face.glyph;b=slot.bitmap
    return (slot.bitmap_left,slot.bitmap_top,b.width,b.rows,b.pitch,bytes(b.buffer))


def enclosed_regions(mask):
    _,_,width,height,pitch,pixels=mask
    holes=0;visited=set()
    for y in range(height):
        for x in range(width):
            if (x,y) in visited or pixels[y*pitch+x]>=128: continue
            stack=[(x,y)];visited.add((x,y));boundary=False
            while stack:
                a,b=stack.pop()
                boundary |= a in (0,width-1) or b in (0,height-1)
                for p,q in ((a-1,b),(a+1,b),(a,b-1),(a,b+1)):
                    if 0<=p<width and 0<=q<height and (p,q) not in visited and pixels[q*pitch+p]<128:
                        visited.add((p,q));stack.append((p,q))
            if not boundary:holes+=1
    return holes


class FontTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries=[]
        for relative in FAMILIES:
            mod=master(ROOT/relative)
            shapes=extend(mod.draw(),mod.STEM,mod.ADVANCE)
            stem=mod.FAMILY.replace(' ','')+'-Regular'
            paths=[ROOT/relative/'fonts'/(stem+'.'+ext) for ext in ('ttf','woff2')]
            cls.entries.append((mod,shapes,paths))

    def test_exact_repertoire_and_nonempty(self):
        for mod,shapes,paths in self.entries:
            for p in paths:
                with self.subTest(font=p.name),TTFont(p) as font:
                    self.assertEqual(set(font.getBestCmap()),{ord(c) for c in COVERAGE})
                    self.assertEqual(font['maxp'].numGlyphs,len(COVERAGE)+1)
                    self.assertGreater(font['glyf']['.notdef'].numberOfContours,0)
                    for c in COVERAGE:
                        self.assertEqual(font['glyf'][glyph_name(c)].numberOfContours==0,c in BLANKS,(p.name,c))

    def test_outlines_match_quantized_master(self):
        for mod,shapes,paths in self.entries:
            for p in paths:
                with TTFont(p) as font:
                    for c,(g,_) in shapes.items():
                        self.assertTrue(g.is_valid,(mod.FAMILY,c))
                        self.assertEqual(outline(font,c),sorted(contours(g)),(p.name,c))

    def test_metrics_and_bounds(self):
        for mod,shapes,paths in self.entries:
            with TTFont(paths[0]) as font:
                self.assertEqual(font['head'].unitsPerEm,1000)
                self.assertEqual(font['head'].created,TIMESTAMP)
                self.assertEqual(font['head'].modified,TIMESTAMP)
                self.assertEqual(font['OS/2'].version,4)
                self.assertEqual(font['OS/2'].fsType,0)
                self.assertTrue(font['OS/2'].fsSelection & 128)
                self.assertEqual(font['post'].isFixedPitch,int(mod.MONO))
                self.assertEqual((font['hhea'].ascent,font['hhea'].descent,font['hhea'].lineGap),(1000,-250,0))
                for c,(g,a) in shapes.items():
                    aw,lsb=font['hmtx'][glyph_name(c)]
                    self.assertEqual(aw,a)
                    self.assertEqual(lsb,int(g.bounds[0]) if not g.is_empty else 0)
                    if mod.MONO:self.assertEqual(aw,mod.ADVANCE)
                    if not g.is_empty:
                        x0,y0,x1,y1=g.bounds
                        self.assertGreaterEqual(x0,0,(mod.FAMILY,c,g.bounds))
                        self.assertLessEqual(x1,aw,(mod.FAMILY,c,g.bounds))
                        self.assertGreaterEqual(y0,-250,(mod.FAMILY,c,g.bounds))
                        self.assertLessEqual(y1,1000,(mod.FAMILY,c,g.bounds))
                self.assertNotIn('GSUB',font)  # No hidden ligatures/substitutions.
                self.assertEqual('GPOS' in font,not mod.MONO)

    def test_names_and_distinct_masters(self):
        identities=[]
        for mod,_,paths in self.entries:
            with TTFont(paths[0]) as font:
                self.assertEqual(font['name'].getDebugName(1),mod.FAMILY)
                self.assertEqual(font['name'].getDebugName(2),'Regular')
                self.assertIn('SIL Open Font License',font['name'].getDebugName(13))
                identities.append(font['name'].getDebugName(6))
        self.assertEqual(len(set(identities)),3)
        for c in 'AaGgM0':
            signatures=[repr(contours(shapes[c][0])) for _,shapes,_ in self.entries]
            self.assertEqual(len(set(signatures)),3,c)

    def test_all_exported_glyphs_render(self):
        # Compare TTF with the decoded WOFF2 through independent FreeType.
        for mod,shapes,paths in self.entries:
            with tempfile.TemporaryDirectory() as tmp:
                decoded=Path(tmp)/'decoded.ttf'
                with TTFont(paths[1]) as f:f.flavor=None;f.save(decoded)
                faces=[freetype.Face(str(paths[0])),freetype.Face(str(decoded))]
                for px in (16,24,48):
                    for c in shapes:
                        a,b=(raster(face,c,px) for face in faces)
                        self.assertEqual(a,b,(mod.FAMILY,c,px))
                        if c not in BLANKS:self.assertTrue(any(a[-1]),(mod.FAMILY,c,px))

    def test_latchline_disambiguation(self):
        mod,shapes,paths=self.entries[0]
        face=freetype.Face(str(paths[0]))
        groups=('Il1|','O0Ø','B8','S5','Z2','gq','b6')
        for chars in groups:
            for a,b in itertools.combinations(chars,2):
                self.assertNotEqual(contours(shapes[a][0]),contours(shapes[b][0]),(a,b))
                for px in (16,18,24):self.assertNotEqual(raster(face,a,px),raster(face,b,px),(a,b,px))

    def test_latchline_counters_survive(self):
        mod,shapes,paths=self.entries[0]
        face=freetype.Face(str(paths[0]))
        for c,minimum in [('O',1),('0',2),('8',2),('B',2),('o',1),('a',1),('g',1)]:
            self.assertGreaterEqual(sum(len(p.interiors) for p in polygons(shapes[c][0])),minimum,c)
            for px in (18,24,32):self.assertGreaterEqual(enclosed_regions(raster(face,c,px)),minimum,(c,px))

    def test_i_accents_replace_dot(self):
        for index in (0,2):
            mod,shapes,_=self.entries[index]
            base=shapes['i'][0].intersection(box(-1000,-1000,2000,600))
            for c in 'ìíîï':
                parts=polygons(shapes[c][0])
                # No old dot may remain: accented-i ink below 600 is base only.
                # Accent can begin below 600 on lowercase; the former dot zone
                # is checked via expected component counts instead of clipping.
                expected=len(polygons(base))+(2 if c=='ï' else 1)
                self.assertEqual(len(parts),expected,(mod.FAMILY,c))

    def test_cell_seams_and_blocks(self):
        for mod,shapes,_ in self.entries:
            for c,arms in BOX_ARMS.items():
                g,a=shapes[c]
                for arm in arms:
                    x,y={'l':(0,350),'r':(a,350),'u':(a/2,1000),'d':(a/2,-250)}[arm]
                    from shapely import Point
                    self.assertTrue(g.covers(Point(x,y)),(mod.FAMILY,c,arm))
            for first,second in [('▀','▄'),('▌','▐')]:
                self.assertTrue(merge(shapes[first][0],shapes[second][0]).equals(shapes['█'][0]))
            density=[shapes[c][0].area for c in '░▒▓█']
            self.assertEqual(density,sorted(density))
            self.assertEqual(len(set(density)),4)

    def test_diecast_spacing_and_case(self):
        mod,shapes,paths=self.entries[1]
        self.assertLess(shapes['I'][1],shapes['M'][1])
        self.assertEqual(len({shapes[c][1] for c in '0123456789'}),1)
        for c in 'abcdefghijklmnopqrstuvwxyz':
            self.assertLess(shapes[c][0].bounds[3],shapes[c.upper()][0].bounds[3])
        for (a,b),kern in KERN.items():
            overlap=shapes[a][0].intersection(translate(shapes[b][0],xoff=shapes[a][1]+kern))
            self.assertAlmostEqual(overlap.area,0,msg=a+b)
        # D retains a flat left wall, unlike chamfered O; not just a name change.
        self.assertNotEqual(contours(shapes['D'][0]),contours(shapes['O'][0]))

    def test_independent_process_reproducibility(self):
        with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
            for output,seed in [(a,'1'),(b,'91827')]:
                env=dict(os.environ,PYTHONHASHSEED=seed)
                subprocess.run([sys.executable,str(ROOT/'tools/original_trio/build.py'),'--output',output],env=env,check=True,stdout=subprocess.PIPE)
            files=sorted(p.relative_to(a) for p in Path(a).rglob('*') if p.is_file())
            self.assertEqual(len(files),7)  # 6 font outputs + manifest.
            for p in files:
                self.assertEqual((Path(a)/p).read_bytes(),(Path(b)/p).read_bytes(),str(p))
                self.assertEqual((ROOT/p).read_bytes(),(Path(a)/p).read_bytes(),f'stale committed output: {p}')

    def test_opentype_sanitizer(self):
        executable=shutil.which('ots-sanitize')
        if not executable:
            if REQUIRE_OTS:self.fail('ots-sanitize is required but missing')
            self.skipTest('ots-sanitize unavailable; hosted CI requires it')
        with tempfile.TemporaryDirectory() as tmp:
            for _,_,paths in self.entries:
                for p in paths:
                    result=subprocess.run([executable,str(p),str(Path(tmp)/(p.name+'.sanitized.ttf'))],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
                    self.assertEqual(result.returncode,0,f'{p.name}: {result.stdout}')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-ots',action='store_true')
    parser.add_argument('--report',type=Path)
    args=parser.parse_args();REQUIRE_OTS=args.require_ots
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(FontTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if args.report:
        report={'schema':1,'successful':result.wasSuccessful(),'tests':result.testsRun,
                'failures':len(result.failures),'errors':len(result.errors),'skipped':[why for _,why in result.skipped],
                'ots_required':REQUIRE_OTS,'versions':{p:importlib.metadata.version(p) for p in ('fonttools','shapely','Brotli','freetype-py')},
                'font_manifest':json.loads((ROOT/'docs/original-trio-manifest.json').read_text(encoding='utf-8'))}
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    sys.exit(not result.wasSuccessful())
