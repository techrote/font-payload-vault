#!/usr/bin/env python3
"""Do not rebuild over committed outputs: verify exact master identity first.
Copyright (c) 2026 techrote. SIL OFL 1.1; see OFL.txt.
"""
from __future__ import annotations
import argparse,hashlib,io,json,os,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
from importlib.metadata import version
from fontTools.ttLib import TTFont
import freetype
from build import ROOT,FAMILIES,COVERAGE,BLANK,master,designs,contours,glyph_name,filename,TIMESTAMP
from engine import union
REQUIRE_OTS=False

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def raster(face,c,px):
    face.set_pixel_sizes(0,px)
    face.load_char(c,freetype.FT_LOAD_RENDER|freetype.FT_LOAD_NO_HINTING)
    g=face.glyph;bm=g.bitmap
    return (g.bitmap_left,g.bitmap_top,bm.width,bm.rows,bm.pitch,bytes(bm.buffer),g.advance.x)

class Qualification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=[]
        for rel in FAMILIES:
            m=master(rel);sh=designs(m)
            cls.data.append((rel,m,sh,[ROOT/rel/'fonts'/(filename(m)+'.'+ext) for ext in ('ttf','woff2')]))

    def test_01_coverage_geometry_and_blank_policy(self):
        for rel,m,sh,paths in self.data:
            self.assertEqual(len(sh),254,rel)
            self.assertEqual(set(sh),COVERAGE,rel)
            for c,(g,adv) in sh.items():
                self.assertTrue(g.is_valid,(rel,c))
                self.assertEqual(g.is_empty,c in BLANK,(rel,c))
                self.assertGreater(adv,0)

    def test_02_advance_and_clip_bounds(self):
        for rel,m,sh,paths in self.data:
            if not m.MONO:self.assertGreater(len({v[1] for v in sh.values()}),3)
            self.assertEqual(len({sh[d][1] for d in '0123456789'}),1,rel)
            for c,(g,adv) in sh.items():
                if m.MONO:self.assertEqual(adv,m.ADVANCE,(rel,c))
                if g.is_empty:continue
                x0,y0,x1,y1=g.bounds
                self.assertGreaterEqual(x0,-.001,(rel,c));self.assertLessEqual(x1,adv+.001,(rel,c))
                self.assertGreaterEqual(y0,-250.001,(rel,c));self.assertLessEqual(y1,1000.001,(rel,c))

    def test_03_font_outlines_and_metrics_match_source(self):
        for rel,m,sh,paths in self.data:
            with TTFont(paths[0],recalcTimestamp=False) as ft:
                for c,(g,adv) in sh.items():
                    glyph=ft['glyf'][glyph_name(c)];rings=contours(g)
                    flat=[pt for ring in rings for pt in ring]
                    if flat:
                        coords,ends,flags=glyph.getCoordinates(ft['glyf'])
                        self.assertEqual(list(map(tuple,coords)),flat,(rel,c))
                        total=0;expected=[]
                        for ring in rings:total+=len(ring);expected.append(total-1)
                        self.assertEqual(list(ends),expected,(rel,c))
                    else:self.assertEqual(glyph.numberOfContours,0)
                    self.assertEqual(ft['hmtx'][glyph_name(c)],(int(adv),int(round(g.bounds[0])) if flat else 0),(rel,c))

    def test_04_open_type_names_and_bits(self):
        ids=set()
        for rel,m,sh,paths in self.data:
            for p in paths:
                with TTFont(p,recalcTimestamp=False) as ft:
                    self.assertEqual(set(ft.getBestCmap()),{ord(c) for c in COVERAGE},rel)
                    self.assertEqual(len(ft.getGlyphOrder()),255);self.assertEqual(ft.getGlyphOrder()[0],'.notdef')
                    self.assertEqual(ft['name'].getDebugName(1),m.FAMILY)
                    self.assertEqual(ft['name'].getDebugName(2),m.STYLE)
                    self.assertEqual(ft['name'].getDebugName(6),filename(m))
                    self.assertEqual(ft['post'].isFixedPitch,int(m.MONO))
                    oblique=m.STYLE=='Oblique'
                    self.assertEqual(ft['OS/2'].fsSelection,0x281 if oblique else 0xC0)
                    self.assertEqual(ft['head'].macStyle,2 if oblique else 0)
                    self.assertEqual(ft['hhea'].caretSlopeRun,212 if oblique else 0)
                    self.assertEqual(ft['OS/2'].fsType,0)
                    self.assertEqual(ft['head'].created,TIMESTAMP);self.assertEqual(ft['head'].modified,TIMESTAMP)
                    self.assertEqual((ft['hhea'].ascent,ft['hhea'].descent,ft['hhea'].lineGap),(1000,-250,0))
                    self.assertNotIn('GSUB',ft);self.assertNotIn('GPOS',ft)
                    self.assertNotIn('fpgm',ft);self.assertNotIn('prep',ft)
            self.assertNotIn(filename(m),ids);ids.add(filename(m))

    def test_05_exact_sha_manifest(self):
        man=json.loads((ROOT/'docs/third-cohort-manifest.json').read_text())
        self.assertEqual(len(man['families']),12)
        for entry,(rel,m,sh,paths) in zip(man['families'],self.data):
            self.assertEqual(entry['family'],m.FAMILY)
            self.assertEqual(entry['style'],m.STYLE);self.assertEqual(entry['codepoints'],254)
            self.assertEqual(entry['glyphs'],255);self.assertEqual(entry['fixed_pitch'],m.MONO)
            self.assertEqual(set(entry['files']),{p.relative_to(ROOT).as_posix() for p in paths})
            for p in paths:
                self.assertEqual(entry['files'][p.relative_to(ROOT).as_posix()],{'sha256':digest(p),'bytes':p.stat().st_size},p.name)

    def test_06_exact_freetype_raster_woff2_equivalence(self):
        count=0
        for rel,m,sh,paths in self.data:
            f=TTFont(paths[1],recalcTimestamp=False);f.flavor=None
            output=io.BytesIO();f.save(output);f.close()
            left=freetype.Face(io.BytesIO(paths[0].read_bytes()))
            right=freetype.Face(io.BytesIO(output.getvalue()))
            for px in (18,36,68):
                for c in sorted(COVERAGE):
                    a=raster(left,c,px);b=raster(right,c,px)
                    self.assertEqual(a,b,(rel,c,px));count+=1
                    self.assertEqual(any(a[5]),c not in BLANK,(rel,c,px))
        self.assertEqual(count,9144)

    def test_07_complete_four_handdrawn_masters(self):
        from masters import TRACE,BUSHING,MICRO,GRID
        core=set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
        for name,d in [('trace',TRACE),('bushing',BUSHING),('micro',MICRO),('grid',GRID)]:
            self.assertEqual(set(d),core,name)
        self.assertEqual(len(set(tuple(d[c] for c in sorted(core)) for d in [TRACE,BUSHING,MICRO,GRID])),4)
        for c,grid in GRID.items():
            self.assertEqual(len(grid.split('/')),9,c)
            for row in grid.split('/'):self.assertEqual(len(row),7,(c,row))

    def test_08_distinct_faces_and_genuine_lowercase(self):
        fingerprints=[]
        for rel,m,sh,paths in self.data:
            fp=tuple((tuple(tuple(r) for r in contours(sh[c][0])),sh[c][1]) for c in 'AaBbDdGgQqOo0123456789')
            self.assertNotIn(fp,fingerprints,rel);fingerprints.append(fp)
            for c in 'abcdefghijklmnopqrstuvwxyz':
                self.assertNotEqual(contours(sh[c][0]),contours(sh[c.upper()][0]),(rel,c))

    def test_09_practical_distinctions_are_visual(self):
        for rel,m,sh,paths in self.data[:3]:
            face=freetype.Face(str(paths[0]));pairs=('Il','I1','I|','l1','O0','B8','gq')
            for px in (20,28,40):
                for a,b in pairs:
                    self.assertNotEqual(raster(face,a,px)[:-1],raster(face,b,px)[:-1],(rel,a,b,px))

    def test_10_mono_box_and_blocks_tile_exactly(self):
        for rel,m,sh,paths in self.data:
            f=sh['█'][0];self.assertEqual(f.bounds,(0.0,-250.0,float(m.ADVANCE if m.MONO else 585),1000.0))
            self.assertTrue(union(sh['▀'][0],sh['▄'][0]).equals(f),rel)
            self.assertTrue(union(sh['▌'][0],sh['▐'][0]).equals(f),rel)

    def test_11_family_specific_features(self):
        for rel,m,sh,paths in self.data:
            if m.MODE=='sling':self.assertEqual(m.STYLE,'Oblique')
            if m.MODE=='haze':self.assertGreater(len(contours(sh['A'][0])),10)
            if m.MODE=='pixel':self.assertGreater(len(contours(sh['B'][0])),5)
            if m.MODE=='bridge':self.assertGreater(len(contours(sh['B'][0])),2)
            if m.MODE=='carbon':
                from masters import MICRO
                from engine import paths_geom
                original=paths_geom(MICRO['E'],m.STEM,cap=2,join=2)
                self.assertLess(sh['E'][0].area,original.area)
            if m.MODE=='ghost':self.assertGreater(len(contours(sh['A'][0])),1)

    def test_12_rebuild_different_hash_seeds_exact_bytes(self):
        for seed in ('17','991'):
            with tempfile.TemporaryDirectory() as td:
                env={**os.environ,'PYTHONHASHSEED':seed}
                cp=subprocess.run([sys.executable,str(ROOT/'tools/third_cohort/build.py'),'--output',td],env=env,capture_output=True,text=True)
                self.assertEqual(cp.returncode,0,cp.stderr[-1800:])
                for rel,m,sh,paths in self.data:
                    for p in paths:self.assertEqual(p.read_bytes(),(Path(td)/p.relative_to(ROOT)).read_bytes(),(rel,p.name,seed))
                self.assertEqual((ROOT/'docs/third-cohort-manifest.json').read_bytes(),(Path(td)/'docs/third-cohort-manifest.json').read_bytes())

    def test_13_open_type_sanitizer(self):
        ots=shutil.which('ots-sanitize')
        if not ots:
            if REQUIRE_OTS:self.fail('Required OpenType Sanitizer binary missing')
            self.skipTest('OTS not installed locally; hosted acceptance requires OTS')
        with tempfile.TemporaryDirectory() as td:
            for rel,m,sh,paths in self.data:
                for p in paths:
                    target=Path(td)/(p.name+'.ttf')
                    result=subprocess.run([ots,str(p),str(target)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
                    self.assertEqual(result.returncode,0,(p.name,result.stdout[-1000:]))

    def test_14_report_manifest_binding(self):
        manifest=json.loads((ROOT/'docs/third-cohort-manifest.json').read_text())
        for file in ('third-cohort-verification.json','third-cohort-browser-verification.json'):
            p=ROOT/'docs'/file
            if p.exists():
                report=json.loads(p.read_text())
                self.assertTrue(report['successful'],file)
                self.assertEqual(report['font_manifest'],manifest,file)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--require-ots',action='store_true');p.add_argument('--report',type=Path)
    args=p.parse_args();REQUIRE_OTS=args.require_ots
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Qualification))
    report={'schema':1,'successful':result.wasSuccessful(),'tests':result.testsRun,
        'failures':len(result.failures),'errors':len(result.errors),'skipped':[reason for _,reason in result.skipped],
        'ots_required':REQUIRE_OTS,'paired_raster_comparisons':12*254*3,
        'versions':{x:version(x) for x in ('fonttools','shapely','Brotli','freetype-py')},
        'font_manifest':json.loads((ROOT/'docs/third-cohort-manifest.json').read_text())}
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(not result.wasSuccessful())
