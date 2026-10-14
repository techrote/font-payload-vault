#!/usr/bin/env python3
"""Fail closed on stale payloads, changed metrics, clipping and invalid exports.
Copyright (c) 2026 techrote. SIL OFL 1.1; see OFL.txt.
"""
from __future__ import annotations
import argparse,hashlib,io,json,os,shutil,subprocess,sys,tempfile,unittest
from collections import deque
from importlib.metadata import version
from pathlib import Path
import freetype
from fontTools.ttLib import TTFont
from build import ROOT,FAMILIES,master,designs,filename,glyph_name,contours,box,merge,COVERAGE,BLANKS,TIMESTAMP

REQUIRE_OTS=False

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def raster(data,c,size):
    face=freetype.Face(io.BytesIO(data));face.set_pixel_sizes(0,size)
    face.load_char(c,freetype.FT_LOAD_RENDER|freetype.FT_LOAD_NO_HINTING)
    g=face.glyph;b=g.bitmap
    return (g.bitmap_left,g.bitmap_top,b.width,b.rows,b.pitch,bytes(b.buffer),g.advance.x)

def counter_count(r):
    _,_,w,h,pitch,data,_=r
    # Flood the padded background; count enclosed background components >= 4 px.
    ink={(x+1,y+1) for y in range(h) for x in range(w) if data[y*pitch+x]>=96}
    seen=set(ink);components=[]
    for y in range(h+2):
        for x in range(w+2):
            if (x,y) in seen:continue
            q=deque([(x,y)]);seen.add((x,y));n=0;outside=False
            while q:
                xx,yy=q.popleft();n+=1
                outside|=xx in (0,w+1) or yy in (0,h+1)
                for p in ((xx-1,yy),(xx+1,yy),(xx,yy-1),(xx,yy+1)):
                    if 0<=p[0]<w+2 and 0<=p[1]<h+2 and p not in seen:seen.add(p);q.append(p)
            if not outside and n>=4:components.append(n)
    return len(components)

class Qualification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items=[]
        for rel in FAMILIES:
            mod=master(rel);sh=designs(mod);paths=[ROOT/rel/'fonts'/(filename(mod)+'.'+ext) for ext in ('ttf','woff2')]
            cls.items.append((rel,mod,sh,paths))

    def test_01_coverage_and_nonempty(self):
        for rel,m,sh,paths in self.items:
            self.assertEqual(set(m.draw()),set(map(chr,range(32,127))),rel)
            self.assertEqual(set(sh),COVERAGE,rel)
            for c,(g,a) in sh.items():
                self.assertEqual(g.is_empty,c in BLANKS,(rel,c))
                self.assertTrue(g.is_valid,(rel,c));self.assertGreater(a,0)

    def test_02_bounds_and_fixed_pitch(self):
        for rel,m,sh,paths in self.items:
            for c,(g,a) in sh.items():
                if m.MONO:self.assertEqual(a,m.ADVANCE,(rel,c))
                if g.is_empty:continue
                x0,y0,x1,y1=g.bounds
                self.assertGreaterEqual(x0,0,(rel,c));self.assertLessEqual(x1,a,(rel,c))
                self.assertGreaterEqual(y0,-250,(rel,c));self.assertLessEqual(y1,1000,(rel,c))
            if not m.MONO:self.assertGreater(len({a for g,a in sh.values()}),3,rel)
            self.assertEqual(len({sh[c][1] for c in '0123456789'}),1,rel)

    def test_03_exact_exported_outlines(self):
        for rel,m,sh,paths in self.items:
            for p in paths:
                with TTFont(p,recalcTimestamp=False) as f:
                    for c,(g,a) in sh.items():
                        glyph=f['glyf'][glyph_name(c)];rings=contours(g)
                        flat=[pt for ring in rings for pt in ring]
                        if flat:
                            coords,ends,flags=glyph.getCoordinates(f['glyf'])
                            self.assertEqual(list(map(tuple,coords)),flat,(p.name,c))
                            count=0;expected=[]
                            for ring in rings:count+=len(ring);expected.append(count-1)
                            self.assertEqual(list(ends),expected,(p.name,c))
                        else:self.assertEqual(glyph.numberOfContours,0)
                        self.assertEqual(f['hmtx'][glyph_name(c)],(a,int(g.bounds[0]) if flat else 0),(p.name,c))

    def test_04_names_metadata_and_style(self):
        ids=set()
        for rel,m,sh,paths in self.items:
            sloped=getattr(m,'STYLE','Regular')=='Oblique'
            for p in paths:
                with TTFont(p,recalcTimestamp=False) as f:
                    self.assertEqual(set(f.getBestCmap()),{ord(c) for c in COVERAGE})
                    self.assertEqual(len(f.getGlyphOrder()),255);self.assertEqual(f.getGlyphOrder()[0],'.notdef')
                    self.assertEqual(f['name'].getDebugName(1),m.FAMILY)
                    self.assertEqual(f['name'].getDebugName(2),getattr(m,'STYLE','Regular'))
                    self.assertEqual(f['name'].getDebugName(6),filename(m))
                    self.assertEqual(f['post'].isFixedPitch,int(m.MONO))
                    self.assertEqual(f['OS/2'].fsType,0)
                    self.assertEqual(f['OS/2'].fsSelection,0x281 if sloped else 0xC0)
                    self.assertEqual(f['head'].macStyle,2 if sloped else 0)
                    self.assertEqual((f['hhea'].caretSlopeRise,f['hhea'].caretSlopeRun),(1000,180 if sloped else 0))
                    self.assertAlmostEqual(f['post'].italicAngle,getattr(m,'ANGLE',0),places=3)
                    self.assertEqual((f['OS/2'].sTypoAscender,f['OS/2'].sTypoDescender,f['OS/2'].sTypoLineGap),(1000,-250,0))
                    self.assertEqual((f['hhea'].ascent,f['hhea'].descent,f['hhea'].lineGap),(1000,-250,0))
                    self.assertEqual(f['head'].modified,TIMESTAMP);self.assertEqual(f['head'].created,TIMESTAMP)
                    self.assertNotIn('GSUB',f);self.assertNotIn('GPOS',f)
                    self.assertNotIn('fpgm',f);self.assertNotIn('prep',f)
            self.assertNotIn(filename(m),ids);ids.add(filename(m))

    def test_05_manifest(self):
        manifest=json.loads((ROOT/'docs/workshop-six-manifest.json').read_text())
        self.assertEqual(manifest['version'],'1.000');self.assertEqual(len(manifest['families']),6)
        for entry,(_,m,sh,paths) in zip(manifest['families'],self.items):
            self.assertEqual(entry['family'],m.FAMILY);self.assertEqual(entry['codepoints'],254)
            self.assertEqual(entry['style'],getattr(m,'STYLE','Regular'))
            self.assertEqual(entry['fixed_pitch'],m.MONO);self.assertEqual(entry['glyphs'],255)
            self.assertEqual(set(entry['files']),{p.relative_to(ROOT).as_posix() for p in paths})
            for p in paths:
                record=entry['files'][p.relative_to(ROOT).as_posix()]
                self.assertEqual(record,{'sha256':digest(p),'bytes':p.stat().st_size})

    def test_06_paired_raster_all_glyphs(self):
        for rel,m,sh,paths in self.items:
            a=paths[0].read_bytes();f=TTFont(paths[1],recalcTimestamp=False);f.flavor=None
            b=io.BytesIO();f.save(b);f.close()
            for size in (16,32,64):
                for c in sorted(COVERAGE):
                    r=raster(a,c,size);other=raster(b.getvalue(),c,size)
                    self.assertEqual(r,other,(rel,c,size))
                    self.assertEqual(any(r[5]),c not in BLANKS,(rel,c,size))

    def test_07_practical_confusables(self):
        pairs=('Il','I1','l1','I|','l|','1|','O0','B8','gq','CG','DO')
        for rel,m,sh,paths in self.items[:2]:
            data=paths[0].read_bytes()
            for size in (18,22,28):
                for a,b in pairs:
                    # Exclude advance: different widths alone cannot pass this test.
                    self.assertNotEqual(raster(data,a,size)[:-1],raster(data,b,size)[:-1],(rel,a,b,size))

    def test_08_practical_raster_counters(self):
        for rel,m,sh,paths in self.items[:2]:
            data=paths[0].read_bytes()
            for size in (22,28,36):
                for c in '0ODPabdo':self.assertGreaterEqual(counter_count(raster(data,c,size)),1,(rel,c,size))
                for c in 'B8':self.assertGreaterEqual(counter_count(raster(data,c,size)),2,(rel,c,size))

    def test_09_rebuild_two_hash_seeds(self):
        for seed in ('17','991'):
            with tempfile.TemporaryDirectory() as td:
                env={**os.environ,'PYTHONHASHSEED':seed}
                subprocess.run([sys.executable,str(ROOT/'tools/workshop_six/build.py'),'--output',td],env=env,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                for rel,m,sh,paths in self.items:
                    for p in paths:self.assertEqual(p.read_bytes(),(Path(td)/p.relative_to(ROOT)).read_bytes(),(rel,p.name,seed))
                self.assertEqual((ROOT/'docs/workshop-six-manifest.json').read_bytes(),(Path(td)/'docs/workshop-six-manifest.json').read_bytes())

    def test_10_ots_all_twelve(self):
        ots=shutil.which('ots-sanitize')
        if not ots:
            if REQUIRE_OTS:self.fail('Required ots-sanitize is unavailable')
            self.skipTest('OTS unavailable locally; hosted acceptance requires it')
        with tempfile.TemporaryDirectory() as td:
            for _,m,sh,paths in self.items:
                for p in paths:
                    result=subprocess.run([ots,str(p),str(Path(td)/(p.name+'.sanitized.ttf'))],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
                    self.assertEqual(result.returncode,0,(p.name,result.stdout))

    def test_11_family_specific_construction(self):
        rel,m,sh,_=self.items[2]
        # Flypress A must have its upper counter, not a solid triangular cap.
        self.assertGreater(len(sh['A'][0].interiors) if sh['A'][0].geom_type=='Polygon' else sum(len(p.interiors) for p in sh['A'][0].geoms),0)
        rel,m,sh,_=self.items[4]
        self.assertEqual(len(m.GRID),95)
        node=m.draw()['.'][0]
        self.assertGreater(len(node.geoms),4)  # emitter + halo remain separate.
        rel,m,sh,_=self.items[5]
        for c in 'aAiìíîï':
            self.assertEqual(sh[c][0].bounds,(27.0,-242.0,733.0,992.0))
            self.assertGreater(sh[c][0].area,300000)
        self.assertTrue(sh[' '][0].is_empty)
        self.assertEqual(sh['─'][0].bounds[0],0)
        self.assertEqual(sh['─'][0].bounds[2],m.ADVANCE)

    def test_12_cell_geometry(self):
        for rel,m,sh,paths in self.items:
            full=sh['█'][0]
            self.assertTrue(merge(sh['▀'][0],sh['▄'][0]).equals(full),rel)
            self.assertTrue(merge(sh['▌'][0],sh['▐'][0]).equals(full),rel)
            self.assertEqual(full.bounds,(0.0,-250.0,float(m.ADVANCE),1000.0))
            self.assertEqual(sh['│'][0].bounds[1::2],(-250.0,1000.0))

    def test_13_six_distinct_alphabets(self):
        fingerprints=[]
        for rel,m,sh,paths in self.items:
            fingerprint=tuple(sh[c][0].wkb for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
            self.assertNotIn(fingerprint,fingerprints);fingerprints.append(fingerprint)
            for c in 'abcdefghijklmnopqrstuvwxyz':self.assertNotEqual(sh[c][0].wkb,sh[c.upper()][0].wkb,(rel,c))

    def test_14_retained_report_binding(self):
        # A stored historical pass must refer to the currently delivered bytes.
        manifest=json.loads((ROOT/'docs/workshop-six-manifest.json').read_text())
        for name in ('workshop-six-verification.json','workshop-six-browser-verification.json'):
            p=ROOT/'docs'/name
            if p.exists():
                report=json.loads(p.read_text());self.assertTrue(report['successful'])
                self.assertEqual(report['font_manifest'],manifest,name)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--require-ots',action='store_true');p.add_argument('--report',type=Path)
    args=p.parse_args();REQUIRE_OTS=args.require_ots
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Qualification))
    report={'schema':1,'successful':result.wasSuccessful(),'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
        'skipped':[reason for _,reason in result.skipped],'ots_required':REQUIRE_OTS,'paired_raster_comparisons':6*254*3,
        'versions':{k:version(k) for k in ('fonttools','shapely','Brotli','freetype-py')},
        'font_manifest':json.loads((ROOT/'docs/workshop-six-manifest.json').read_text())}
    if args.report:args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
