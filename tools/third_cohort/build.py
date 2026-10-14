#!/usr/bin/env python3
"""Reproducible twelve-font builder, with distinct source-drawn treatments.
Source masters and named family overrides reside in this new cohort.
Copyright (c) 2026 techrote. SIL OFL 1.1; see OFL.txt.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import newTable
from shapely.geometry import Polygon, MultiPolygon
from shapely.geometry.polygon import orient
from engine import drawn_ascii,extend,COVERAGE,BLANK,fit
ROOT=Path(__file__).resolve().parents[2]
VERSION='1.000';TIMESTAMP=3874780800
CATEGORIES=(
 ('cmd-font-container',('tracebar-mono','bushing-sans','microslab','nibble-nine')),
 ('hot-font-box',('torque-plate','sling-arc','swarf-bridge','raster-forge')),
 ('cachemonic',('shift-ghost','eddy-notch','carbon-check','checksum-haze'))
)

FAMILIES=tuple(f'{cat}/{slug}' for cat,slugs in CATEGORIES for slug in slugs)

def master(rel):
    spec=importlib.util.spec_from_file_location(rel.replace('/','_').replace('-','_'),ROOT/rel/'source/design.py')
    if spec is None or spec.loader is None:raise RuntimeError(f'Could not import {rel}')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod

def designs(mod):return extend(drawn_ascii(mod),mod)
def filename(mod):return mod.FAMILY.replace(' ','')+'-'+mod.STYLE

def glyph_name(c):return f'uni{ord(c):04X}'

def contours(geom):
    if geom.is_empty:return []
    polygons=list(geom.geoms) if hasattr(geom,'geoms') else [geom]
    polygons=[p for p in polygons if isinstance(p,Polygon) and p.area>2]
    polygons.sort(key=lambda p:(round(p.bounds[0],3),round(p.bounds[1],3),round(p.area,2)))
    rings=[]
    for raw in polygons:
        p=orient(raw,sign=-1)
        for line in [p.exterior,*p.interiors]:
            pts=[]
            for x,y in list(line.coords)[:-1]:
                q=(round(x),round(y))
                if not pts or pts[-1]!=q:pts.append(q)
            if len(pts)>1 and pts[0]==pts[-1]:pts.pop()
            if len(pts)>=3 and abs(sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts))))>3:
                rings.append(pts)
    return rings

def notdef(adv):
    from shapely.geometry import box
    outside=box(90,0,adv-90,750)
    inside=box(152,67,adv-152,682)
    return outside.difference(inside)

def make_font(mod,shape):
    glyphs={};metrics={};order=['.notdef']+[glyph_name(c) for c in sorted(shape)]
    source={'.notdef':(notdef(mod.ADVANCE),mod.ADVANCE),**{glyph_name(c):v for c,v in shape.items()}}
    for name,(g,adv) in source.items():
        pen=TTGlyphPen(None)
        for ring in contours(g):
            pen.moveTo(ring[0]);[pen.lineTo(pt) for pt in ring[1:]];pen.closePath()
        glyphs[name]=pen.glyph()
        metrics[name]=(int(adv),int(round(g.bounds[0])) if not g.is_empty else 0)
    fb=FontBuilder(1000,isTTF=True);fb.setupGlyphOrder(order)
    fb.setupCharacterMap({ord(c):glyph_name(c) for c in shape});fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    isoblique=mod.STYLE=='Oblique'
    fb.setupHorizontalHeader(ascent=1000,descent=-250,lineGap=0,caretSlopeRise=1000,caretSlopeRun=212 if isoblique else 0)
    fb.setupNameTable({
        'familyName':mod.FAMILY,'styleName':mod.STYLE,
        'uniqueFontIdentifier':f'techrote:{filename(mod)}:{VERSION}',
        'fullName':mod.FAMILY+' '+mod.STYLE,'psName':filename(mod),
        'version':'Version '+VERSION,
        'typographicFamily':mod.FAMILY,'typographicSubfamily':mod.STYLE,
        'copyright':'Copyright (c) 2026 techrote. All rights reserved.',
        'manufacturer':'font-payload-vault',
        'designer':'techrote / AI-assisted procedural original art',
        'description':f'Third Cohort original masters, design: {mod.CATEGORY}/{mod.SLUG}/DESIGN.md',
        'licenseDescription':'SIL Open Font License 1.1. No Reserved Font Names.',
        'licenseInfoURL':'https://openfontlicense.org',
        'vendorURL':'https://github.com/techrote/font-payload-vault'})
    fb.setupOS2(version=4,sTypoAscender=1000,sTypoDescender=-250,sTypoLineGap=0,usWinAscent=1000,usWinDescent=250,
        sxHeight=540,sCapHeight=730,usWeightClass=400,usWidthClass=5,fsType=0,fsSelection=0x281 if isoblique else 0xC0,achVendID='fpvt')
    fb.setupPost(isFixedPitch=int(mod.MONO),italicAngle=-12 if isoblique else 0,underlinePosition=-170,underlineThickness=55)
    fb.setupMaxp();fb.font['head'].macStyle=2 if isoblique else 0
    gasp=newTable('gasp');gasp.gaspRange={65535:3};fb.font['gasp']=gasp
    fb.font['head'].created=TIMESTAMP;fb.font['head'].modified=TIMESTAMP;fb.font['head'].fontRevision=1.0
    fb.font.recalcTimestamp=False
    return fb.font

def build(output=ROOT):
    records=[]
    for rel in FAMILIES:
        m=master(rel);shape=designs(m);font=make_font(m,shape)
        dest=Path(output)/rel/'fonts';dest.mkdir(parents=True,exist_ok=True);files={}
        for ext,flavor in [('ttf',None),('woff2','woff2')]:
            target=dest/(filename(m)+'.'+ext);font.flavor=flavor;font.save(target)
            files[target.relative_to(output).as_posix()]={'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size}
        font.close()
        records.append({'family':m.FAMILY,'style':m.STYLE,'category':m.CATEGORY,'lineage':m.LINEAGE,'mode':m.MODE,
                        'codepoints':len(shape),'glyphs':len(shape)+1,'fixed_pitch':m.MONO,'files':files})
        print(f'{m.FAMILY}: {len(shape)} codepoints, TTF + WOFF2',flush=True)
    man={'schema':1,'version':VERSION,'families':records}
    p=Path(output)/'docs/third-cohort-manifest.json';p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(man,indent=2)+'\n',encoding='utf-8')
    return man

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT)
    build(p.parse_args().output.resolve())
