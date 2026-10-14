#!/usr/bin/env python3
"""Path-based proofs and offline interactive testers from the compiled fonts.
Copyright (c) 2026 techrote. SIL OFL 1.1; see OFL.txt.
"""
from __future__ import annotations
import argparse
import html
import json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from build import ROOT, FAMILIES, config, filename, COVERAGE

class Proof:
    def __init__(self, rel):
        self.cfg=config(rel);self.font=TTFont(ROOT/rel/'fonts'/(filename(self.cfg)+'.ttf'),recalcTimestamp=False)
        self.glyphs=self.font.getGlyphSet();self.cmap=self.font.getBestCmap();self.seen=set()
    def width(self,text,size):
        return sum(self.font['hmtx'][self.cmap.get(ord(c),'.notdef')][0] for c in text)*size/1000
    def text(self,text,x,y,size,color='#18252d',max_width=None):
        if max_width: size=min(size,size*max_width/max(1,self.width(text,size)))
        result=[]
        for c in text:
            name=self.cmap.get(ord(c),'.notdef');ident=filename(self.cfg)+'_'+name
            if ident not in self.seen:
                pen=SVGPathPen(self.glyphs);self.glyphs[name].draw(pen)
                result.append(f'<defs><path id="{ident}" d="{pen.getCommands()}"/></defs>');self.seen.add(ident)
            result.append(f'<use href="#{ident}" transform="translate({x:.4f} {y}) scale({size/1000:.5f} {-size/1000:.5f})" fill="{color}"/>')
            x+=self.font['hmtx'][name][0]*size/1000
        return '\n'.join(result)

def label(text,x,y,size=16,color='#51636b'):
    return f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" fill="{color}">{html.escape(text)}</text>'
def svg(width,height,title,parts):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{html.escape(title)}</title>\n'+'\n'.join(parts)+'\n</svg>\n'

def sheet(proof):
    proof.seen.clear();c=proof.cfg
    parts=['<rect width="1540" height="1420" fill="#f6f4ed"/>',label(c['family']+' / '+c['style']+' / Fifth Cohort',42,36,21)]
    parts += [proof.text(c['family'],42,139,92,max_width=1456),label(c['tagline'],42,181,19)]
    for text,y,size in [('ABCDEFGHIJKLMNOPQRSTUVWXYZ',277,49),('abcdefghijklmnopqrstuvwxyz',368,49),
                         ('0123456789  Il1|  O0  B8  CG  DO  gq  rn m',462,43),
                         ('.,:; !? @#$% &* ()[]{} <> += / \\ | ~',559,43),
                         ('ÀÁÂÃÄÅ Ç ÈÉÊË ÌÍÎÏ Ñ ÒÓÔÕÖ Ø ÙÚÛÜ Ý ß',665,34),
                         ('àáâãäå ç èéêë ìíîï ñ òóôõö ø ùúûü ýÿ',744,34),
                         ('£ € ¥ ¢ © ® ½ ¼ ¾ ± − ≠ ≤ ≥ ← ↑ → ↓ ✓',833,38)]:
        parts.append(proof.text(text,42,y,size,max_width=1456))
    parts.append(label('Size ladder / inspection, not approval of every size. Trial: '+str(c['trial'][0])+'–'+str(c['trial'][1])+' px',42,908,18))
    y=960
    for size in (18,24,36,52):
        parts.append(label(str(size)+' px',42,y));parts.append(proof.text('Pack my box / 0123456789',137,y,size));y+=size*1.5+38
    parts.append(label('Unhinted outlines. No Windows, accessibility, distance-legibility or fabrication acceptance is implied.',42,1385,16))
    return svg(1540,1420,c['family']+' proof',parts)

def charmap(proof):
    proof.seen.clear();parts=['<rect width="1470" height="2200" fill="#f6f4ed"/>',label(proof.cfg['family']+' / all 254 mapped codepoints',30,42,24)]
    for i,c in enumerate(sorted(COVERAGE)):
        x=24+i%14*102;y=102+i//14*109
        parts.append(f'<rect x="{x}" y="{y-26}" width="98" height="106" fill="none" stroke="#cbd1ce"/>')
        parts.append(label(f'U+{ord(c):04X}',x+5,y-7,12))
        parts.append(proof.text(c,x+8,y+53,57,max_width=83))
    return svg(1470,2200,proof.cfg['family']+' character map',parts)

TEMPLATE='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ — Fifth Cohort tester</title>
<style>
:root{color-scheme:light dark}body{margin:0;padding:24px;background:#f6f4ed;color:#18252d;font:16px system-ui,sans-serif}body.dark{background:#131e25;color:#f6f4ed}main{max-width:1440px;margin:auto}h1{font-size:28px}textarea{width:100%;box-sizing:border-box;min-height:140px;font:18px monospace;padding:12px}fieldset{display:flex;flex-wrap:wrap;gap:18px;margin:20px 0;border:1px solid #84969b}label{display:block}input,button{font:inherit}button{padding:4px 12px}#preview{display:block;padding:16px 0;white-space:pre-wrap;overflow-wrap:anywhere;font-synthesis:none}#status,#missing{padding:8px 0}#missing{color:#a42f35}body.dark #missing{color:#ffb4b4}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(88px,1fr));gap:6px}.cell{border:1px solid #98a5a7;text-align:center;padding:5px;overflow:hidden}.cell span{display:block;font-size:40px;line-height:1.5;font-synthesis:none}.cell small{font:11px monospace}
</style></head><body><main>
<h1>__TITLE__ / __STYLE__</h1><p>__TAGLINE__</p><p>Trial range: __TRIAL__. This loads the adjacent WOFF2 without a CDN. Unsupported characters use fallback and are warned below.</p>
<p id="status" role="status">Loading font…</p><label for="input">Your text</label><textarea id="input" spellcheck="false"></textarea>
<fieldset><legend>Preview controls</legend>
<label>Size <input id="size" type="range" min="12" max="160" value="52"><span id="sizeValue"></span></label>
<label>Line height <input id="line" type="range" min="1" max="2" step="0.05" value="1.25"></label>
<label>Tracking <input id="tracking" type="range" min="0" max="10" step="0.25" value="0"></label>
<label><input id="polarity" type="checkbox"> Dark background</label><button id="reset" type="button">Reset text and controls</button>
</fieldset><p id="missing" role="status"></p><output id="preview" aria-live="polite"></output>
<h2>Complete repertoire — 254 codepoints</h2><div class="grid" id="grid"></div>
<p>Read the parent README.md and DESIGN.md for source provenance, rebuild commands and limits. First-release unhinted outlines: no kerning or ligatures, no general combining-mark shaping, and no native Windows or human-factor acceptance.</p>
<script>
'use strict';
const cfg=__CONFIG__;const get=id=>document.getElementById(id);const supported=new Set(cfg.coverage);
function style(node){node.style.fontFamily='"'+cfg.family+'", monospace';node.style.fontStyle=cfg.style;}
function update(){const text=get('input').value;get('preview').textContent=text;
get('preview').style.fontSize=get('size').value+'px';get('preview').style.lineHeight=get('line').value;get('preview').style.letterSpacing=get('tracking').value+'px';get('sizeValue').textContent=get('size').value+' px';document.body.classList.toggle('dark',get('polarity').checked);
const missing=[...new Set(Array.from(text).map(c=>c.codePointAt(0)).filter(c=>!supported.has(c)&&![9,10,13].includes(c)))];get('missing').textContent=missing.length?'Not in this font: '+missing.map(c=>'U+'+c.toString(16).toUpperCase().padStart(4,'0')).join(', '):'';}
function reset(){get('input').value=cfg.sample;get('size').value='52';get('line').value='1.25';get('tracking').value='0';get('polarity').checked=false;update();}
style(get('preview'));get('reset').addEventListener('click',reset);
for(const id of ['input','size','line','tracking','polarity'])get(id).addEventListener('input',update);
for(const cp of cfg.coverage){const cell=document.createElement('div');cell.className='cell';const code=document.createElement('small');code.textContent='U+'+cp.toString(16).toUpperCase().padStart(4,'0');const glyph=document.createElement('span');glyph.textContent=String.fromCodePoint(cp);style(glyph);cell.append(code,glyph);get('grid').append(cell);}
reset();const face=new FontFace(cfg.family,'url('+cfg.url+')',{style:cfg.style});
face.load().then(font=>{document.fonts.add(font);get('status').dataset.loaded='true';get('status').textContent='Font loaded: '+cfg.family+' / '+cfg.label;}).catch(()=>{get('status').dataset.loaded='false';get('status').textContent='FONT LOAD FAILED — keep the specimen and fonts folders together. Fallback is not this font.';});
</script></main></body></html>
'''

def tester(c):
    cfg=dict(family=c['family'],style='oblique' if c['style']=='Oblique' else 'normal',label=c['style'],
      coverage=sorted(map(ord,COVERAGE)),url='../fonts/'+filename(c)+'.woff2',
      sample=c['family']+'\n'+c['sample']+'\nThe quick brown fox jumps over the lazy dog.\n0123456789 Il1| O0 B8 gq\nÀÉÎÖÜ àéîöü £ € ± →')
    return TEMPLATE.replace('__TITLE__',html.escape(c['family'])).replace('__STYLE__',c['style']).replace('__TAGLINE__',html.escape(c['tagline'])).replace('__TRIAL__',str(c['trial'][0])+'–'+str(c['trial'][1])+' px').replace('__CONFIG__',json.dumps(cfg,ensure_ascii=True).replace('</','<\\/'))

def outputs():
    out={};overview=['<rect width="1570" height="2820" fill="#f6f4ed"/>',label('FONT PAYLOAD VAULT / FIFTH COHORT / TWELVE FACES, SIX NEW LINEAGES',38,43,20)]
    for i,rel in enumerate(FAMILIES):
        p=Proof(rel);c=p.cfg
        out[rel+'/specimen/specimen.svg']=sheet(p)
        out[rel+'/specimen/character-map.svg']=charmap(p)
        out[rel+'/specimen/index.html']=tester(c)
        p.seen.clear();y=83+i*225
        overview += [f'<path d="M38 {y} H1532" stroke="#cad3d0"/>',label(f'{i+1:02} / '+c['family']+' / '+c['style']+' / '+c['lineage']+' lineage',38,y+28,18)]
        overview += [p.text(c['family'],38,y+106,76,max_width=1490),p.text(c['sample'],38,y+160,33,max_width=1490),p.text('Aa Bb Gg Qq 0123456789  Il1| O0 B8',38,y+205,33,max_width=1490)]
        p.font.close()
    out['docs/fifth-cohort-overview.svg']=svg(1570,2820,'Fifth Cohort: twelve new typefaces',overview)
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    data=outputs()
    for rel,text in data.items():
        p=ROOT/rel
        if args.check:
            if not p.exists() or p.read_text(encoding='utf-8')!=text:raise SystemExit('STALE SPECIMEN: '+rel)
        else:p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
    print(str(len(data))+' specimen outputs '+('verified' if args.check else 'generated'))
