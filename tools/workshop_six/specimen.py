#!/usr/bin/env python3
"""Deterministic path proofs and offline testers from the compiled TTF payloads.
Copyright (c) 2026 techrote. SIL OFL 1.1; see OFL.txt.
"""
from __future__ import annotations
import argparse,html,json
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from build import ROOT,FAMILIES,master,filename,COVERAGE

class Proof:
    def __init__(self,relative):
        self.mod=master(relative)
        self.font=TTFont(ROOT/relative/'fonts'/(filename(self.mod)+'.ttf'),recalcTimestamp=False)
        self.glyphs=self.font.getGlyphSet();self.cmap=self.font.getBestCmap();self.seen=set()
    def reset(self):self.seen.clear()
    def text(self,text,x,y,size,fill='#182024'):
        parts=[];pos=x
        for c in text:
            name=self.cmap.get(ord(c),'.notdef');pen=SVGPathPen(self.glyphs);self.glyphs[name].draw(pen)
            d=pen.getCommands()
            if d:
                ident=filename(self.mod)+'_'+name
                if ident not in self.seen:
                    parts.append(f'<defs><path id="{ident}" d="{d}"/></defs>');self.seen.add(ident)
                parts.append(f'<use href="#{ident}" transform="translate({pos:.3f} {y}) scale({size/1000:.4f} {-size/1000:.4f})" fill="{fill}"/>')
            pos+=self.font['hmtx'][name][0]*size/1000
        return '\n'.join(parts)
    def width(self,text,size):return sum(self.font['hmtx'][self.cmap.get(ord(c),'.notdef')][0] for c in text)*size/1000
    def fit(self,text,size,width):return min(size,size*width/max(1,self.width(text,size)))

def label(text,x,y,size=18,fill='#46545b'):
    return f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" fill="{fill}">{html.escape(text)}</text>'
def svg(width,height,parts,title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{html.escape(title)}</title>\n'+'\n'.join(parts)+'\n</svg>\n'

def sheet(proof):
    proof.reset();m=proof.mod;parts=['<rect width="1500" height="1160" fill="#f6f4ee"/>',label(m.FAMILY+' / '+getattr(m,'STYLE','Regular')+' / original master',45,35)]
    parts+=[proof.text(m.FAMILY.upper(),45,142,proof.fit(m.FAMILY.upper(),82,1410)),label(m.TAGLINE,45,185)]
    for text,y,size in [('ABCDEFGHIJKLMNOPQRSTUVWXYZ',269,48),('abcdefghijklmnopqrstuvwxyz',350,48),('0123456789  Il1|  O0Q  B8  gq  rn m',435,43),('.,:; !? @#$% &* ()[]{} <> += / \\ | ~',522,40),('ÀÁÂÃÄÅ Ç ÈÉÊË ÌÍÎÏ Ñ ÒÓÔÕÖ Ø ÙÚÛÜ Ý ß',613,34),('àáâãäå ç èéêë ìíîï ñ òóôõö ø ùúûü ýÿ',688,34)]:
        parts.append(proof.text(text,45,y,proof.fit(text,size,1410)))
    parts.append(label('Size ladder — inspection samples, not approval of every size. Trial range: '+m.TRIAL,45,751))
    y=795
    for size in (16,24,36,48):
        text='The quick brown fox jumps over the lazy dog. 0123456789'
        parts.append(label(str(size)+' px',45,y,15));parts.append(proof.text(text,135,y,proof.fit(text,size,1320)));y+=size*1.5+18
    return svg(1500,1160,parts,m.FAMILY+' full specimen')

def character_map(proof):
    proof.reset();chars=sorted(COVERAGE);rows=(len(chars)+15)//16;parts=['<rect width="1440" height="'+str(95+rows*119)+'" fill="#f6f4ee"/>',label(proof.mod.FAMILY+' / complete 254-codepoint repertoire',30,39,23)]
    for i,c in enumerate(chars):
        x=24+(i%16)*87;y=100+(i//16)*119
        parts.append(f'<rect x="{x}" y="{y-27}" width="85" height="116" fill="none" stroke="#cbd0d0"/>')
        parts.append(label(f'{ord(c):04X}',x+7,y-9,12))
        parts.append(proof.text(c,x+6,y+65,min(61,73*1000/proof.font['hmtx'][proof.cmap[ord(c)]][0])))
    return svg(1440,95+rows*119,parts,proof.mod.FAMILY+' character map')

TEMPLATE='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ — local specimen</title>
<style>
:root{color-scheme:light dark}body{margin:0;padding:24px;background:#f6f4ee;color:#182024;font:16px system-ui,sans-serif}body.dark{background:#101417;color:#f4f0e8}main{max-width:1400px;margin:auto}h1{font-size:28px}textarea{box-sizing:border-box;width:100%;min-height:130px;font:18px monospace;padding:12px}fieldset{margin:18px 0;display:flex;flex-wrap:wrap;gap:20px;border:1px solid #88949b}label{display:block}output{display:block;padding:18px 0;white-space:pre-wrap;overflow-wrap:anywhere;font-synthesis:none}#status,#missing{padding:8px 0}#missing{color:#a53d29}body.dark #missing{color:#ffaa8e}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(86px,1fr));gap:6px}.cell{border:1px solid #8b969e;text-align:center;padding:5px;overflow:hidden}.cell span{display:block;font-size:38px;line-height:1.5;font-synthesis:none}.cell small{font:11px monospace}button{font:inherit;padding:5px 12px}
</style></head><body><main>
<h1>__TITLE__</h1><p>__TAGLINE__</p><p>Open this file from a local checkout; it loads only the adjacent WOFF2. Trial range: __TRIAL__. No Windows or human-factors acceptance is implied.</p>
<p id="status" role="status">Loading font…</p>
<label for="input">Your text</label><textarea id="input" spellcheck="false"></textarea>
<fieldset><legend>Preview controls</legend>
<label>Size <input id="size" type="range" min="12" max="120" value="48"><span id="sizeValue"></span></label>
<label>Line height <input id="line" type="range" min="1" max="2" step="0.05" value="1.25"></label>
<label>Tracking <input id="tracking" type="range" min="0" max="8" step="0.25" value="0"></label>
<label><input id="polarity" type="checkbox"> Dark background</label><button id="reset" type="button">Reset sample</button>
</fieldset><p id="missing" role="status"></p><output id="preview" aria-live="polite"></output>
<h2>Complete repertoire — 254 codepoints</h2><div id="grid" class="grid"></div>
<p>Sources, design rationale and limitations are in the parent README.md and DESIGN.md. Unsupported characters are shown by fallback and warned above. No ligatures or pair kerning are present in these first releases.</p>
<script>
'use strict';
const cfg=__CONFIG__;
const el=id=>document.getElementById(id);const supported=new Set(cfg.coverage);let ready=false;
const style=node=>{node.style.fontFamily='"'+cfg.family+'", monospace';node.style.fontStyle=cfg.style;};
function update(){
 const text=el('input').value;el('preview').textContent=text;
 el('preview').style.fontSize=el('size').value+'px';el('preview').style.lineHeight=el('line').value;el('preview').style.letterSpacing=el('tracking').value+'px';el('sizeValue').textContent=el('size').value+' px';
 document.body.classList.toggle('dark',el('polarity').checked);
 const missing=[...new Set(Array.from(text).map(c=>c.codePointAt(0)).filter(c=>!supported.has(c)&&![9,10,13].includes(c)))];
 el('missing').textContent=missing.length?'Not in this font: '+missing.map(c=>'U+'+c.toString(16).toUpperCase().padStart(4,'0')).join(', '):'';
}
style(el('preview'));el('input').value=cfg.sample;
for(const id of ['input','size','line','tracking','polarity'])el(id).addEventListener('input',update);
el('reset').addEventListener('click',()=>{el('input').value=cfg.sample;update();});
for(const cp of cfg.coverage){const cell=document.createElement('div');cell.className='cell';const small=document.createElement('small');small.textContent='U+'+cp.toString(16).toUpperCase().padStart(4,'0');const glyph=document.createElement('span');glyph.textContent=String.fromCodePoint(cp);style(glyph);cell.append(small,glyph);el('grid').append(cell);}
update();
const face=new FontFace(cfg.family,'url('+cfg.url+')',{style:cfg.style});
face.load().then(font=>{document.fonts.add(font);ready=true;el('status').textContent='Font loaded: '+cfg.family+' / '+cfg.label;el('status').dataset.loaded='true';}).catch(()=>{el('status').textContent='FONT LOAD FAILED — keep specimen and fonts folders together. Display is fallback, not the specimen font.';el('status').dataset.loaded='false';});
</script></main></body></html>
'''

def tester(m):
    cfg={'family':m.FAMILY,'style':'oblique' if getattr(m,'STYLE','Regular')=='Oblique' else 'normal','label':getattr(m,'STYLE','Regular'),
        'url':'../fonts/'+filename(m)+'.woff2','coverage':sorted(map(ord,COVERAGE)),'sample':'\n'.join(m.SAMPLES)}
    return TEMPLATE.replace('__TITLE__',html.escape(m.FAMILY)).replace('__TAGLINE__',html.escape(m.TAGLINE)).replace('__TRIAL__',m.TRIAL).replace('__CONFIG__',json.dumps(cfg,ensure_ascii=True).replace('</','<\\/'))

def outputs():
    out={};proofs=[]
    for rel in FAMILIES:
        p=Proof(rel);proofs.append(p)
        for name,text in [('specimen.svg',sheet(p)),('character-map.svg',character_map(p)),('index.html',tester(p.mod))]:out[rel+'/specimen/'+name]=text
    parts=['<rect width="1480" height="1900" fill="#101417"/>',label('FONT PAYLOAD VAULT / WORKSHOP SIX / ORIGINAL TYPEFACES',52,52,20,'#d7e0e4')]
    for i,p in enumerate(proofs):
        p.reset();y=104+i*290;m=p.mod
        parts.append(f'<path d="M52 {y}H1428" stroke="#53616b"/>')
        parts.append(label(f'{i+1:02}  {m.SLUG}  /  {getattr(m,"STYLE","Regular")}',52,y+35,20,'#b2bbc4'))
        for text,baseline,size in [(m.FAMILY.upper(),y+120,70),(m.SAMPLES[1],y+196,38),('Aa Bb Gg Qq  0123456789  Il1| O0',y+263,28)]:
            if m.FAMILY=='Null Cartridge':size*=.85
            parts.append(p.text(text,52,baseline,p.fit(text,size,1360),'#f4f0e8'))
        p.font.close()
    out['docs/workshop-six-overview.svg']=svg(1480,1900,parts,'Workshop Six: the complete new cohort')
    return out

def main(check=False):
    for rel,text in outputs().items():
        p=ROOT/rel
        if check:
            if not p.exists() or p.read_text(encoding='utf-8')!=text:raise SystemExit('STALE SPECIMEN: '+rel)
        else:p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
    print('19 specimen outputs '+('verified' if check else 'generated'))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');main(p.parse_args().check)
