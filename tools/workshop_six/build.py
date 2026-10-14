#!/usr/bin/env python3
"""Build the six new families from their own source masters, not other fonts.
Copyright (c) 2026 techrote. SIL OFL 1.1; see OFL.txt.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import newTable
from common import *
from repertoire import extend,COVERAGE,BLANKS
ROOT=Path(__file__).resolve().parents[2]
FAMILIES=('cmd-font-container/collet-sans','cmd-font-container/detent-slab','hot-font-box/flypress','hot-font-box/ribbon-torque','cachemonic/anode-bloom','cachemonic/null-cartridge')
VERSION='1.000';TIMESTAMP=3874780800

def master(relative):
    spec=importlib.util.spec_from_file_location(relative.replace('/','_').replace('-','_'),ROOT/relative/'source/design.py')
    if spec is None or spec.loader is None:raise RuntimeError(relative)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod

def designs(mod):
    core=mod.draw()
    result=extend(core,mod.STEM,mod.ADVANCE)
    if hasattr(mod,'finalize'):result={c:(mod.finalize(c,g,a),a) for c,(g,a) in result.items()}
    return {c:(clean(g),a) for c,(g,a) in result.items()}

def glyph_name(c):return 'uni'+f'{ord(c):04X}'
def filename(mod):return mod.FAMILY.replace(' ','')+'-'+getattr(mod,'STYLE','Regular')

def make_font(mod,shapes):
    glyphs={};metrics={};order=['.notdef']+[glyph_name(c) for c in sorted(shapes)]
    n=box(75,0,mod.ADVANCE-75,720).difference(box(143,68,mod.ADVANCE-143,652))
    n=merge(n,stroke([(154,91),(mod.ADVANCE-154,629)],55))
    source={'.notdef':(n,mod.ADVANCE),**{glyph_name(c):v for c,v in shapes.items()}}
    for name,(g,a) in source.items():
        pen=TTGlyphPen(None)
        for pts in contours(g):
            pen.moveTo(pts[0])
            for p in pts[1:]:pen.lineTo(p)
            pen.closePath()
        glyphs[name]=pen.glyph();metrics[name]=(a,int(g.bounds[0]) if not g.is_empty else 0)
    fb=FontBuilder(1000,isTTF=True);fb.setupGlyphOrder(order)
    fb.setupCharacterMap({ord(c):glyph_name(c) for c in shapes});fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics);fb.setupHorizontalHeader(ascent=1000,descent=-250,lineGap=0,caretSlopeRise=1000,caretSlopeRun=180 if getattr(mod,'STYLE','Regular')=='Oblique' else 0)
    style=getattr(mod,'STYLE','Regular');sloped=style=='Oblique'
    fb.setupNameTable({'familyName':mod.FAMILY,'styleName':style,'uniqueFontIdentifier':f'techrote:{filename(mod)}:{VERSION}',
        'fullName':mod.FAMILY+' '+style,'psName':filename(mod),'version':'Version '+VERSION,
        'typographicFamily':mod.FAMILY,'typographicSubfamily':style,
        'copyright':'Copyright (c) 2026 techrote. All rights reserved.',
        'manufacturer':'font-payload-vault','designer':'techrote / AI-assisted original design',
        'description':f'Workshop Six original master; sources and limits: {mod.SLUG}/DESIGN.md',
        'licenseDescription':'SIL Open Font License 1.1. No Reserved Font Names.',
        'licenseInfoURL':'https://openfontlicense.org','vendorURL':'https://github.com/techrote/font-payload-vault'})
    fb.setupOS2(version=4,sTypoAscender=1000,sTypoDescender=-250,sTypoLineGap=0,usWinAscent=1000,usWinDescent=250,
        sxHeight=mod.X_HEIGHT,sCapHeight=mod.CAP_HEIGHT,usWeightClass=400,usWidthClass=3 if mod.FAMILY=='Flypress' else 5,
        fsType=0,fsSelection=0x281 if sloped else 0xC0,achVendID='fpvt')
    fb.setupPost(isFixedPitch=int(mod.MONO),italicAngle=getattr(mod,'ANGLE',0),underlinePosition=-175,underlineThickness=60)
    fb.setupMaxp();fb.font['head'].macStyle=2 if sloped else 0
    gasp=newTable('gasp');gasp.gaspRange={65535:3};fb.font['gasp']=gasp
    fb.font['head'].created=TIMESTAMP;fb.font['head'].modified=TIMESTAMP;fb.font['head'].fontRevision=1.0;fb.font.recalcTimestamp=False
    return fb.font

def build(output=ROOT):
    records=[]
    for relative in FAMILIES:
        mod=master(relative);shapes=designs(mod);font=make_font(mod,shapes)
        dest=Path(output)/relative/'fonts';dest.mkdir(parents=True,exist_ok=True);files={}
        for ext,flavor in [('ttf',None),('woff2','woff2')]:
            target=dest/(filename(mod)+'.'+ext);font.flavor=flavor;font.save(target)
            files[target.relative_to(output).as_posix()]={'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size}
        records.append({'family':mod.FAMILY,'style':getattr(mod,'STYLE','Regular'),'codepoints':len(shapes),'glyphs':len(shapes)+1,'fixed_pitch':mod.MONO,'files':files})
        print(f'{mod.FAMILY}: {len(shapes)} codepoints / TTF + WOFF2')
    p=Path(output)/'docs/workshop-six-manifest.json';p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps({'schema':1,'version':VERSION,'families':records},indent=2)+'\n',encoding='utf-8')
    return records
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT)
    build(p.parse_args().output.resolve())
