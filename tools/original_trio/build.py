#!/usr/bin/env python3
"""Build only the three original families; never read another font as input.
Copyright (c) 2026 techrote. SIL Open Font License 1.1; see OFL.txt.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.ttLib import newTable
from geometry import box, merge, stroke, contours
from repertoire import extend

ROOT = Path(__file__).resolve().parents[2]
FAMILIES = ('cmd-font-container/latchline-mono','hot-font-box/diecast-relay','cachemonic/cache-rattle')
TIMESTAMP = 3874780800  # 2026-10-14 00:00:00 UTC in the OpenType 1904 epoch.
VERSION = '1.000'
KERN = {'AV':-32,'AW':-24,'AY':-28,'AT':-24,'VA':-32,'WA':-24,'YA':-28,'TA':-24,'To':-20,'Te':-20}


def master(folder):
    spec=importlib.util.spec_from_file_location(folder.name.replace('-','_'),folder/'source/design.py')
    if spec is None or spec.loader is None:
        raise RuntimeError(f'Cannot load {folder}')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def glyph_name(c):
    return 'uni'+f'{ord(c):04X}'


def make_font(mod, shapes):
    order=['.notdef']+[glyph_name(c) for c in sorted(shapes)]
    notdef=box(90,0,mod.ADVANCE-90,700).difference(box(155,65,mod.ADVANCE-155,635))
    notdef=merge(notdef,stroke([(170,130),(mod.ADVANCE-170,570)],55))
    designs={'.notdef':(notdef,mod.ADVANCE)}
    designs.update({glyph_name(c):v for c,v in shapes.items()})
    glyphs={}; metrics={}
    for name,(g,advance) in designs.items():
        pen=TTGlyphPen(None)
        for pts in contours(g):
            pen.moveTo(pts[0])
            for p in pts[1:]: pen.lineTo(p)
            pen.closePath()
        glyphs[name]=pen.glyph()
        metrics[name]=(advance,int(g.bounds[0]) if not g.is_empty else 0)
    fb=FontBuilder(1000,isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({ord(c):glyph_name(c) for c in shapes})
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=1000,descent=-250,lineGap=0)
    ps=mod.FAMILY.replace(' ','')+'-Regular'
    fb.setupNameTable({
        'familyName':mod.FAMILY,'styleName':'Regular','uniqueFontIdentifier':f'techrote:{ps}:{VERSION}',
        'fullName':mod.FAMILY+' Regular','psName':ps,'version':'Version '+VERSION,
        'typographicFamily':mod.FAMILY,'typographicSubfamily':'Regular',
        'copyright':'Copyright (c) 2026 techrote. All rights reserved.',
        'manufacturer':'font-payload-vault','designer':'techrote / AI-assisted original design',
        'description':f'Original procedural typeface. Sources and limitations: {mod.SLUG}/DESIGN.md.',
        'licenseDescription':'Licensed under the SIL Open Font License, Version 1.1. No Reserved Font Names.',
        'licenseInfoURL':'https://openfontlicense.org',
        'vendorURL':'https://github.com/techrote/font-payload-vault',
    })
    fb.setupOS2(version=4,sTypoAscender=1000,sTypoDescender=-250,sTypoLineGap=0,usWinAscent=1000,usWinDescent=250,
                sxHeight=mod.X_HEIGHT,sCapHeight=mod.CAP_HEIGHT,usWeightClass=400,
                usWidthClass=5,fsType=0,fsSelection=0xC0,achVendID='FPVT')
    fb.setupPost(isFixedPitch=int(mod.MONO),underlinePosition=-155,underlineThickness=60)
    fb.setupMaxp()
    if not mod.MONO:
        pairs='\n'.join(f'pos {glyph_name(a)} {glyph_name(b)} {value};' for (a,b),value in KERN.items())
        addOpenTypeFeaturesFromString(fb.font,'languagesystem DFLT dflt; languagesystem latn dflt; feature kern {\n'+pairs+'\n} kern;')
    gasp=newTable('gasp');gasp.gaspRange={65535:3};fb.font['gasp']=gasp
    fb.font['head'].created=TIMESTAMP;fb.font['head'].modified=TIMESTAMP
    fb.font['head'].fontRevision=1.0
    fb.font.recalcTimestamp=False
    return fb.font


def build(output_root=ROOT):
    info=[]
    for relative in FAMILIES:
        folder=ROOT/relative;mod=master(folder)
        shapes=extend(mod.draw(),mod.STEM,mod.ADVANCE)
        font=make_font(mod,shapes)
        out=Path(output_root)/relative/'fonts';out.mkdir(parents=True,exist_ok=True)
        stem=mod.FAMILY.replace(' ','')+'-Regular'
        files={}
        for ext,flavor in [('ttf',None),('woff2','woff2')]:
            font.flavor=flavor
            target=out/(stem+'.'+ext);font.save(target)
            files[target.relative_to(output_root).as_posix()]={'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size}
        item={'family':mod.FAMILY,'version':VERSION,'codepoints':len(shapes),'glyphs':len(shapes)+1,
              'fixed_pitch':mod.MONO,'files':files}
        info.append(item)
        print(f'{mod.FAMILY}: {len(shapes)} characters; TTF + WOFF2')
    destination=Path(output_root)/'docs/original-trio-manifest.json'
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps({'schema':1,'families':info},indent=2)+'\n',encoding='utf-8')
    return info


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT,help='output root (source root stays unchanged)')
    args=parser.parse_args();build(args.output.resolve())
