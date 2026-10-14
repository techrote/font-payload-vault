#!/usr/bin/env python3
"""Fail-closed Fifth Cohort software qualification; never overwrite font inputs.
Copyright (c) 2026 techrote. SIL OFL 1.1; see OFL.txt.
"""
from __future__ import annotations
import argparse
from collections import deque
import hashlib
import io
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from importlib.metadata import version
import freetype
from fontTools.ttLib import TTFont
from build import ROOT,FAMILIES,config,filename,glyph_name,sha256,source_fingerprints,TIMESTAMP
from common import (designs,raw_alphabet,MASTERS,LETTERS_DIGITS,ASCII,COVERAGE,BLANKS,
                    contours,merge,box,Polygon,LineString,paths,stitched,hatch,nib,grid_shape,FUNCTIONAL)
REQUIRE_OTS=False
REQUIRE_RECORDS=False
SIZES=(18,36,68)


def raster(face, c):
    face.load_char(c, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING)
    g=face.glyph;b=g.bitmap
    return (g.bitmap_left,g.bitmap_top,b.width,b.rows,b.pitch,bytes(b.buffer),g.advance.x)


def counter_count(r):
    _,_,w,h,pitch,data,_=r
    ink={(x+1,y+1) for y in range(h) for x in range(w) if data[y*pitch+x]>=96}
    seen=set(ink);n_holes=0
    for y in range(h+2):
        for x in range(w+2):
            if (x,y) in seen:continue
            seen.add((x,y));q=deque([(x,y)]);outside=False;count=0
            while q:
                xx,yy=q.popleft();count+=1;outside |= xx in (0,w+1) or yy in (0,h+1)
                for p in ((xx-1,yy),(xx+1,yy),(xx,yy-1),(xx,yy+1)):
                    if 0<=p[0]<w+2 and 0<=p[1]<h+2 and p not in seen:seen.add(p);q.append(p)
            if not outside and count>=4:n_holes+=1
    return n_holes


def components(g):
    if g.is_empty:return 0
    return 1 if g.geom_type=='Polygon' else sum(components(p) for p in g.geoms)

class Qualification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items=[]
        for rel in FAMILIES:
            cfg=config(rel);sh,adj=designs(cfg)
            files=[ROOT/rel/'fonts'/(filename(cfg)+'.'+ext) for ext in ('ttf','woff2')]
            cls.items.append((rel,cfg,sh,adj,files))
        cls.manifest=json.loads((ROOT/'docs/fifth-cohort-manifest.json').read_text(encoding='utf-8'))

    def test_01_six_complete_original_masters(self):
        self.assertEqual(len(MASTERS),6);fingerprints=set()
        for name,m in MASTERS.items():
            drawings=getattr(m,'PATHS',getattr(m,'GRID',{}))
            self.assertEqual(set(drawings),LETTERS_DIGITS,name)
            fp=tuple(sorted(drawings.items()));self.assertNotIn(fp,fingerprints);fingerprints.add(fp)
            if name=='pinfeed':
                for c,d in drawings.items():
                    self.assertTrue(11<=len(d.split('/'))<=14,c)
                    for row in d.split('/'):self.assertEqual(len(row),8);self.assertFalse(set(row)-set('.#'))
            else:
                for c,spec in drawings.items():self.assertTrue(paths(spec),(name,c))

    def test_02_repertoire_and_nonempty(self):
        self.assertEqual(len(COVERAGE),254)
        for rel,cfg,sh,adj,files in self.items:
            self.assertEqual(set(sh),COVERAGE,rel)
            for c,(g,a) in sh.items():
                self.assertEqual(g.is_empty,c in BLANKS,(rel,c));self.assertTrue(g.is_valid,(rel,c))
                self.assertIn(g.geom_type,('Polygon','MultiPolygon'),(rel,c,g.geom_type))
                self.assertGreater(a,0)

    def test_03_bounds_and_pitch(self):
        for rel,cfg,sh,adj,files in self.items:
            for c,(g,a) in sh.items():
                if cfg['mono']:self.assertEqual(a,cfg['advance'],(rel,c))
                if g.is_empty:continue
                x0,y0,x1,y1=g.bounds
                self.assertTrue(0<=x0<x1<=a,(rel,c,g.bounds,a))
                self.assertTrue(-250<=y0<y1<=1000,(rel,c,g.bounds))
            if not cfg['mono']:self.assertGreater(len({a for g,a in sh.values()}),10,rel)
            self.assertEqual({sh[c][1] for c in '0123456789'},{cfg['advance']},rel)

    def test_04_exact_exported_contours_and_metrics(self):
        for rel,cfg,sh,adj,files in self.items:
            for p in files:
                with TTFont(p,recalcTimestamp=False) as f:
                    for c,(g,a) in sh.items():
                        gl=f['glyf'][glyph_name(c)];rings=contours(g);flat=[point for ring in rings for point in ring]
                        if not flat:self.assertEqual(gl.numberOfContours,0)
                        else:
                            coords,ends,flags=gl.getCoordinates(f['glyf'])
                            self.assertEqual(list(map(tuple,coords)),flat,(p.name,c))
                            count=0;expected=[]
                            for ring in rings:count+=len(ring);expected.append(count-1)
                            self.assertEqual(list(ends),expected,(p.name,c));self.assertTrue(all(flag&1 for flag in flags))
                        self.assertEqual(f['hmtx'][glyph_name(c)],(a,int(g.bounds[0]) if flat else 0),(p.name,c))
                    self.assertGreater(f['glyf']['.notdef'].numberOfContours,0)

    def test_05_metadata_names_and_style(self):
        names=set()
        for rel,cfg,sh,adj,files in self.items:
            self.assertNotIn(filename(cfg),names);names.add(filename(cfg))
            slope=cfg['style']=='Oblique'
            for p in files:
                with TTFont(p,recalcTimestamp=False) as f:
                    self.assertEqual(set(f.getBestCmap()),set(map(ord,COVERAGE)))
                    self.assertEqual(len(f.getGlyphOrder()),255);self.assertEqual(f.getGlyphOrder()[0],'.notdef')
                    for key,value in ((1,cfg['family']),(2,cfg['style']),(6,filename(cfg)),(16,cfg['family']),(17,cfg['style'])):
                        self.assertEqual(f['name'].getDebugName(key),value,(p.name,key))
                    self.assertEqual(f['post'].isFixedPitch,int(cfg['mono']))
                    self.assertEqual(f['OS/2'].fsType,0);self.assertEqual(f['OS/2'].fsSelection,0x281 if slope else 0xC0)
                    self.assertEqual(f['head'].macStyle,2 if slope else 0)
                    self.assertEqual((f['hhea'].caretSlopeRise,f['hhea'].caretSlopeRun),(1000,round(cfg['shear']*1000)))
                    self.assertAlmostEqual(f['post'].italicAngle,-math.degrees(math.atan(cfg['shear'])),places=3)
                    self.assertEqual((f['OS/2'].sTypoAscender,f['OS/2'].sTypoDescender,f['OS/2'].sTypoLineGap),(1000,-250,0))
                    self.assertEqual((f['hhea'].ascent,f['hhea'].descent,f['hhea'].lineGap),(1000,-250,0))
                    self.assertEqual(f['OS/2'].sCapHeight,round(sh['H'][0].bounds[3]));self.assertEqual(f['OS/2'].sxHeight,round(sh['x'][0].bounds[3]))
                    self.assertEqual(f['head'].unitsPerEm,1000)
                    self.assertEqual((f['head'].created,f['head'].modified),(TIMESTAMP,TIMESTAMP))
                    for t in ('GPOS','GSUB','fpgm','prep','EBDT','EBLC','fvar'):self.assertNotIn(t,f)

    def test_06_hash_and_source_manifest(self):
        self.assertEqual(self.manifest['schema'],1);self.assertEqual(self.manifest['version'],'1.000')
        self.assertEqual(self.manifest['source_sha256'],source_fingerprints())
        self.assertEqual(len(self.manifest['families']),12)
        for entry,(rel,cfg,sh,adj,files) in zip(self.manifest['families'],self.items):
            for k,v in [('family',cfg['family']),('style',cfg['style']),('lineage',cfg['lineage']),('codepoints',254),('glyphs',255),('fixed_pitch',cfg['mono'])]:self.assertEqual(entry[k],v)
            self.assertEqual(entry['vertical_fits'],{f'U+{ord(c):04X}':v for c,v in sorted(adj.items())})
            self.assertEqual(set(entry['files']),{p.relative_to(ROOT).as_posix() for p in files})
            for p in files:self.assertEqual(entry['files'][p.relative_to(ROOT).as_posix()],dict(sha256=sha256(p),bytes=p.stat().st_size))

    def test_07_all_9144_paired_raster_comparisons(self):
        count=0
        for rel,cfg,sh,adj,files in self.items:
            a=freetype.Face(str(files[0]))
            with TTFont(files[1],recalcTimestamp=False) as f:
                f.flavor=None;out=io.BytesIO();f.save(out)
            b=freetype.Face(io.BytesIO(out.getvalue()))
            for size in SIZES:
                a.set_pixel_sizes(0,size);b.set_pixel_sizes(0,size)
                for c in sorted(COVERAGE):
                    r=raster(a,c);self.assertEqual(r,raster(b,c),(rel,c,size))
                    self.assertEqual(any(r[5]),c not in BLANKS,(rel,c,size));count+=1
        self.assertEqual(count,9144)

    def test_08_practical_confusables(self):
        pairs=('Il','I1','l1','I|','l|','1|','O0','B8','gq','CG','DO')
        for rel,cfg,sh,adj,files in self.items[:4]:
            face=freetype.Face(str(files[0]))
            for size in (18,24,32):
                face.set_pixel_sizes(0,size)
                for a,b in pairs:self.assertNotEqual(raster(face,a)[:-1],raster(face,b)[:-1],(rel,a,b,size))

    def test_09_practical_enclosed_counters(self):
        for rel,cfg,sh,adj,files in self.items[:4]:
            face=freetype.Face(str(files[0]))
            for size in (24,32,40):
                face.set_pixel_sizes(0,size)
                for c in '0ODPabdo':self.assertGreaterEqual(counter_count(raster(face,c)),1,(rel,c,size))
                for c in 'B8':self.assertGreaterEqual(counter_count(raster(face,c)),2,(rel,c,size))

    def test_10_functional_cell_geometry(self):
        for rel,cfg,sh,adj,files in self.items:
            full=sh['█'][0]
            self.assertEqual(full.bounds,(0,-250,cfg['advance'],1000))
            self.assertTrue(merge(sh['▀'][0],sh['▄'][0]).equals(full))
            self.assertTrue(merge(sh['▌'][0],sh['▐'][0]).equals(full))
            self.assertEqual(sh['│'][0].bounds[1::2],(-250,1000))
            self.assertEqual(sh['─'][0].bounds[0::2],(0,cfg['advance']))

    def test_11_distinct_final_alphabets_and_true_lowercase(self):
        fps=set()
        for rel,cfg,sh,adj,files in self.items:
            fp=tuple(sh[c][0].wkb for c in sorted(LETTERS_DIGITS));self.assertNotIn(fp,fps,rel);fps.add(fp)
            for c in 'abcdefghijklmnopqrstuvwxyz':self.assertNotEqual(sh[c][0].wkb,sh[c.upper()][0].wkb,(rel,c))

    def test_12_path_parser_rejects_malformed_sources(self):
        for spec in ('','L 1 2','M 1','M 1 2','C 1 2 3 4 5 6','M 0 0 C 1 2','M 0 0 Q 1 2 3 4','M 0 0 Z'):
            with self.assertRaises(ValueError,msg=spec):paths(spec)

    def test_13_stitches_remain_separated(self):
        g=stitched('M 0 0 L 600 0')
        self.assertEqual(components(g),4)
        pieces=sorted(g.geoms,key=lambda p:p.bounds[0])
        for a,b in zip(pieces,pieces[1:]):self.assertGreater(a.distance(b),25)
        # Prevent rounded caps closing the intended gaps again.
        cfg=config(FAMILIES[10]);self.assertGreater(components(raw_alphabet(cfg)['H']),6)

    def test_14_grid_and_weave_geometry(self):
        self.assertEqual(grid_shape('#......./........').area,3600)
        weave=grid_shape('#......./........',True)
        self.assertGreater(weave.area,1800);self.assertLess(weave.area,3300)
        for idx in (3,9):
            raw=raw_alphabet(config(FAMILIES[idx]));g=raw['i']
            self.assertTrue(g.intersection(box(-1000,600,2000,600)).is_empty)
            self.assertGreater(g.intersection(box(-1000,600,2000,1000)).area,1500)

    def test_15_serif_flange_hatch_and_cairn(self):
        raw=raw_alphabet(config(FAMILIES[2]));self.assertGreaterEqual(raw['I'].bounds[2]-raw['I'].bounds[0],160)
        cfg=config(FAMILIES[4]);raw=raw_alphabet(cfg)
        self.assertGreater(raw['H'].area,nib(MASTERS['rail'].PATHS['H'],140,110,cap='flat',join='bevel').area)
        rect=box(0,0,320,600);hg=hatch(rect)
        self.assertEqual(hg.bounds,rect.bounds);self.assertLess(hg.area,rect.area*.65);self.assertGreater(hg.area,rect.area*.20)
        self.assertTrue(rect.difference(rect.buffer(-17)).difference(hg).area<.01)
        raw=raw_alphabet(config(FAMILIES[11]));self.assertGreater(components(raw['O']),8)
        # Explicit faceted i/j dots retain real ink, not one-unit flat-cap remnants.
        for idx in (7,11):
            raw=raw_alphabet(config(FAMILIES[idx]))
            for c in 'ij':self.assertGreater(raw[c].intersection(box(-1000,610,2000,1000)).area,1000)

    def test_16_vertical_fits_are_nonclipping(self):
        for rel,cfg,sh,adj,files in self.items:
            for c,record in adj.items():
                self.assertNotIn(c,FUNCTIONAL);self.assertTrue(0<record['scale_y']<=1)
                self.assertGreaterEqual(sh[c][0].bounds[1],-242);self.assertLessEqual(sh[c][0].bounds[3],984)

    def test_17_unchanged_shared_helpers(self):
        expected={'geometry.py':'e4710922a3e6288024a4335b7f5c1334e7fdeca3','repertoire.py':'b7116c38eee71038d566f0ebf2b9a213475519be'}
        for name,want in expected.items():
            b=(ROOT/'tools/original_trio'/name).read_bytes()
            actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
            self.assertEqual(actual,want,name)

    def test_18_two_independent_rebuilds(self):
        for seed in ('17','991'):
            with tempfile.TemporaryDirectory() as td:
                subprocess.run([sys.executable,str(ROOT/'tools/fifth_cohort/build.py'),'--output',td],
                  env={**os.environ,'PYTHONHASHSEED':seed},check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                for rel,cfg,sh,adj,files in self.items:
                    for p in files:self.assertEqual(p.read_bytes(),(Path(td)/p.relative_to(ROOT)).read_bytes(),(p.name,seed))
                self.assertEqual((ROOT/'docs/fifth-cohort-manifest.json').read_bytes(),(Path(td)/'docs/fifth-cohort-manifest.json').read_bytes())

    def test_19_mandatory_ots_all_24_exports(self):
        ots=shutil.which('ots-sanitize')
        if not ots:
            if REQUIRE_OTS:self.fail('Mandatory ots-sanitize unavailable')
            self.skipTest('OTS unavailable locally; mandatory hosted acceptance remains required')
        with tempfile.TemporaryDirectory() as td:
            for rel,cfg,sh,adj,files in self.items:
                for p in files:
                    r=subprocess.run([ots,str(p),str(Path(td)/(p.name+'.sanitized'))],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
                    self.assertEqual(r.returncode,0,(p.name,r.stdout))

    def test_20_retained_evidence_bound_to_delivered_bytes(self):
        for name in ('fifth-cohort-verification.json','fifth-cohort-browser-verification.json'):
            p=ROOT/'docs'/name
            if REQUIRE_RECORDS:self.assertTrue(p.exists(),'Required retained evidence absent: '+name)
            if p.exists():
                r=json.loads(p.read_text(encoding='utf-8'));self.assertIs(r['successful'],True)
                self.assertEqual(r['font_manifest'],self.manifest)
                if name=='fifth-cohort-verification.json':
                    self.assertEqual(r['tests'],20);self.assertEqual(r['failures'],0);self.assertEqual(r['errors'],0)
                    self.assertEqual(r['skipped'],[]);self.assertTrue(r['ots_required'])
                else:
                    self.assertEqual(len(r['families']),12)
                    self.assertEqual({x['family'] for x in r['families']},{cfg['family'] for _,cfg,_,_,_ in self.items})
                    for entry in r['families']:
                        self.assertEqual(entry['repertoire_cells'],254)
                        for field in ('http_font_load','file_font_load','actual_family_selected','literal_text_not_html','missing_unicode_warning','controls','polarity','full_reset','visible_font_failure'):
                            self.assertIs(entry[field],True)
                        self.assertEqual(entry['external_requests'],[]);self.assertEqual(entry['script_errors'],[])

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--require-ots',action='store_true')
    p.add_argument('--require-records',action='store_true');p.add_argument('--report',type=Path);args=p.parse_args()
    REQUIRE_OTS=args.require_ots;REQUIRE_RECORDS=args.require_records
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Qualification))
    report=dict(schema=1,successful=result.wasSuccessful(),tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),
      skipped=[why for _,why in result.skipped],ots_required=REQUIRE_OTS,paired_raster_comparisons=9144,
      versions={k:version(k) for k in ('fonttools','shapely','Brotli','freetype-py')},
      font_manifest=json.loads((ROOT/'docs/fifth-cohort-manifest.json').read_text(encoding='utf-8')))
    if args.report:args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
