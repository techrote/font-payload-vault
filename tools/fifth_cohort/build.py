#!/usr/bin/env python3
"""Build Fifth Cohort original sources deterministically as TTF + WOFF2.
Copyright (c) 2026 techrote. SIL OFL 1.1; see OFL.txt.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import newTable
from common import designs, contours, box, nib, merge, clean, COVERAGE, BLANKS
from catalog import FAMILIES
ROOT = Path(__file__).resolve().parents[2]
VERSION = '1.000'
TIMESTAMP = 3874780800


def config(rel):
    file=ROOT/rel/'source/design.py'
    spec=importlib.util.spec_from_file_location(rel.replace('/','_').replace('-','_'),file)
    if spec is None or spec.loader is None: raise RuntimeError(str(file))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return dict(module.CONFIG)


def filename(cfg): return cfg['family'].replace(' ','')+'-'+cfg['style']
def glyph_name(c): return 'uni'+f'{ord(c):04X}'
def sha256(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def make_font(cfg, shapes):
    nd=box(70,0,cfg['advance']-70,710).difference(box(134,64,cfg['advance']-134,646))
    nd=merge(nd,nib(f"M 159 100 L {cfg['advance']-159} 610",48))
    data={'.notdef':(nd,cfg['advance']),**{glyph_name(c):shapes[c] for c in sorted(shapes)}}
    glyphs={};metrics={}
    for name,(g,advance) in data.items():
        pen=TTGlyphPen(None);rings=contours(g)
        for ring in rings:
            pen.moveTo(ring[0])
            for pt in ring[1:]: pen.lineTo(pt)
            pen.closePath()
        glyphs[name]=pen.glyph();metrics[name]=(advance,int(g.bounds[0]) if rings else 0)
    fb=FontBuilder(1000,isTTF=True);fb.setupGlyphOrder(list(data))
    fb.setupCharacterMap({ord(c):glyph_name(c) for c in shapes})
    fb.setupGlyf(glyphs);fb.setupHorizontalMetrics(metrics)
    slope=round(1000*cfg['shear']);angle=-math.degrees(math.atan(cfg['shear']));oblique=cfg['style']=='Oblique'
    fb.setupHorizontalHeader(ascent=1000,descent=-250,lineGap=0,caretSlopeRise=1000,caretSlopeRun=slope)
    fb.setupNameTable(dict(familyName=cfg['family'],styleName=cfg['style'],
      uniqueFontIdentifier='techrote:'+filename(cfg)+':'+VERSION,fullName=cfg['family']+' '+cfg['style'],
      psName=filename(cfg),version='Version '+VERSION,typographicFamily=cfg['family'],typographicSubfamily=cfg['style'],
      copyright='Copyright (c) 2026 techrote.',designer='techrote / AI-assisted original design',
      manufacturer='Font Payload Vault',description='Fifth Cohort; original '+cfg['lineage']+' lineage; see repository DESIGN.md.',
      licenseDescription='SIL Open Font License 1.1. No Reserved Font Names.',licenseInfoURL='https://openfontlicense.org',
      vendorURL='https://github.com/techrote/font-payload-vault'))
    fb.setupOS2(version=4,sTypoAscender=1000,sTypoDescender=-250,sTypoLineGap=0,usWinAscent=1000,usWinDescent=250,
      sxHeight=cfg['x_height'],sCapHeight=cfg['cap_height'],usWeightClass=400,usWidthClass=5,
      fsType=0,fsSelection=0x281 if oblique else 0xC0,achVendID='fpvt')
    fb.setupPost(isFixedPitch=int(cfg['mono']),italicAngle=angle,underlinePosition=-186,underlineThickness=54)
    fb.setupMaxp();fb.font['head'].macStyle=2 if oblique else 0
    fb.font['head'].created=TIMESTAMP;fb.font['head'].modified=TIMESTAMP
    fb.font['head'].fontRevision=1.0;fb.font.recalcTimestamp=False
    gasp=newTable('gasp');gasp.gaspRange={65535:3};fb.font['gasp']=gasp
    return fb.font


def source_fingerprints():
    paths=list((ROOT/'tools/fifth_cohort/masters').glob('*.py'))
    paths += [ROOT/rel/'source/design.py' for rel in FAMILIES]
    paths += [ROOT/'tools/fifth_cohort/common.py',ROOT/'tools/fifth_cohort/build.py',ROOT/'tools/fifth_cohort/catalog.py',
              ROOT/'tools/original_trio/geometry.py',ROOT/'tools/original_trio/repertoire.py']
    return {p.relative_to(ROOT).as_posix():sha256(p) for p in sorted(paths)}


def build(output=ROOT):
    records=[]
    for rel in FAMILIES:
        cfg=config(rel);shapes,adjustments=designs(cfg)
        if set(shapes)!=COVERAGE: raise ValueError('Coverage mismatch')
        for c,(g,a) in shapes.items():
            if g.is_empty != (c in BLANKS): raise ValueError((rel,c,'empty'))
            if not g.is_empty:
                x0,y0,x1,y1=g.bounds
                if not 0<=x0<x1<=a or not -250<=y0<y1<=1000: raise ValueError((rel,c,g.bounds,a))
        font=make_font(cfg,shapes);files={}
        target=output/rel/'fonts';target.mkdir(parents=True,exist_ok=True)
        for ext,flavor in [('ttf',None),('woff2','woff2')]:
            p=target/(filename(cfg)+'.'+ext);font.flavor=flavor;font.save(p)
            files[p.relative_to(output).as_posix()]={'sha256':sha256(p),'bytes':p.stat().st_size}
        records.append(dict(family=cfg['family'],style=cfg['style'],lineage=cfg['lineage'],codepoints=len(shapes),
          glyphs=len(shapes)+1,fixed_pitch=cfg['mono'],vertical_fits={f'U+{ord(c):04X}':v for c,v in sorted(adjustments.items())},files=files))
        font.close();print(cfg['family'],len(shapes),'codepoints',sum(x['bytes'] for x in files.values()),'bytes',flush=True)
    manifest=dict(schema=1,version=VERSION,source_sha256=source_fingerprints(),families=records)
    p=output/'docs/fifth-cohort-manifest.json';p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return manifest

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT)
    build(parser.parse_args().output.resolve())
