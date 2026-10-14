#!/usr/bin/env python3
"""Deterministic source-linked vector specimens and local HTML type testers.
Every displayed type glyph is extracted from the built font, not a system fallback.
Copyright (c) 2026 techrote. SIL OFL 1.1; see OFL.txt.
"""
from __future__ import annotations
import argparse,html,json
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from build import ROOT,FAMILIES,master,filename,COVERAGE

class Proof:
    def __init__(self,rel):
        self.m=master(rel)
        self.f=TTFont(ROOT/rel/'fonts'/(filename(self.m)+'.ttf'),recalcTimestamp=False)
        self.glyphs=self.f.getGlyphSet();self.cmap=self.f.getBestCmap();self.seen=set()
    def reset(self):self.seen=set()
    def text(self,txt,x,y,size,fill='#172127'):
        pieces=[];pos=x
        for c in txt:
            name=self.cmap.get(ord(c),'.notdef')
            if name in self.glyphs:
                pen=SVGPathPen(self.glyphs);self.glyphs[name].draw(pen);d=pen.getCommands()
                if d:
                    ident=filename(self.m)+'_'+name
                    if ident not in self.seen:
                        pieces.append(f'<defs><path id="{ident}" d="{d}"/></defs>');self.seen.add(ident)
                    pieces.append(f'<use href="#{ident}" transform="translate({pos:.2f} {y}) scale({size/1000:.4f} {-size/1000:.4f})" fill="{fill}"/>')
                pos+=self.f['hmtx'][name][0]*size/1000
        return '\n'.join(pieces)
    def fitted(self,txt,size,maxwidth):
        width=sum(self.f['hmtx'][self.cmap.get(ord(c),'.notdef')][0] for c in txt)*size/1000
        return min(size,size*maxwidth/max(width,1))

def label(txt,x,y,size=17,fill='#53616d'):
    return f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" fill="{fill}">{html.escape(txt)}</text>'

def svg(w,h,parts,title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{html.escape(title)}</title>\n'+'\n'.join(parts)+'\n</svg>\n'

def specimen(p):
    p.reset();m=p.m
    samples=[('ABCDEFGHIJKLMNOPQRSTUVWXYZ',269,54),('abcdefghijklmnopqrstuvwxyz',370,54),('0123456789  Il1| O0 B8 gq',478,60),('!@#$% &amp;*()[]{};:,.?/+=<>',583,48),('ÀÁÂÃÄÅ Ç ÈÉÊË ÌÍÎÏ Ñ ÒÓÔÕÖ Ø ÙÚÛÜ Ý Ÿ',691,38),('àáâãäå ç èéêë ìíîï ñ òóôõö ø ùúûü ýÿ',780,38)]
    parts=['<rect width="1500" height="1300" fill="#f5f3ed"/>',label(m.FAMILY+' / '+m.STYLE+' / '+m.LINEAGE+' / '+m.MODE,50,45,25),p.text(m.FAMILY.upper(),50,151,p.fitted(m.FAMILY.upper(),100,1370)),label(m.TAGLINE,50,197)]
    for s,y,size in samples:parts.append(p.text(html.unescape(s),50,y,p.fitted(html.unescape(s),size,1390)))
    parts.append(label('Inspection ladder — target trial: '+m.TRIAL+', not certified for all sizes.',50,834))
    for i,(size,y) in enumerate([(18,882),(24,953),(36,1047),(56,1170)]):
        message='The quick brown fox jumps over the lazy dog. 0123456789'
        parts.append(label(str(size)+' px',50,y,17));parts.append(p.text(message,150,y,p.fitted(message,size,1300)))
    return svg(1500,1300,parts,m.FAMILY+' specimen')

def character_map(p):
    p.reset();chars=sorted(COVERAGE);rows=(len(chars)+15)//16;h=100+rows*114
    parts=[f'<rect width="1450" height="{h}" fill="#f5f3ed"/>',label(p.m.FAMILY+' / all '+str(len(chars))+' mapped characters',35,38,23)]
    for i,c in enumerate(chars):
        x=25+(i%16)*88;y=103+(i//16)*114
        parts.append(f'<rect x="{x}" y="{y-33}" width="86" height="108" fill="none" stroke="#c5cccb"/>')
        parts.append(label(f'{ord(c):04X}',x+5,y-13,13))
        name=p.cmap[ord(c)];width=p.f['hmtx'][name][0]
        parts.append(p.text(c,x+6,y+58,min(59,73*1000/width)))
    return svg(1450,h,parts,p.m.FAMILY+' complete glyph repertoire')

HTML='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__FAMILY__ — local type tester</title><style>
:root{color-scheme:light dark}*{box-sizing:border-box}body{margin:0;padding:25px;background:#f5f3ed;color:#16232a;font:16px system-ui,sans-serif}body.dark{background:#121820;color:#e8e8e0}main{max-width:1380px;margin:auto}h1{font-size:30px}textarea{width:100%;min-height:135px;padding:12px;font:18px ui-monospace,monospace}fieldset{display:flex;flex-wrap:wrap;gap:22px;margin:15px 0}label{display:block}#preview{display:block;white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.2;min-height:120px}#status,#missing{margin:10px 0}#missing{color:#ad392d}body.dark #missing{color:#ffbaa8}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(78px,1fr));gap:5px}.cell{border:1px solid #96a09e;text-align:center;padding:4px}.cell small{font:11px ui-monospace,monospace;display:block}.cell b{font-weight:normal;display:block;line-height:1.4;font-size:38px;font-synthesis:none}button{font:inherit;padding:6px 11px}
</style></head><body><main><h1>__FAMILY__ / __STYLE__</h1><p>__TAGLINE__</p><p>One original font (TTF + WOFF2). Suggested trial: __TRIAL__. Native Windows / accessibility acceptance not claimed.</p><p id="status" role="status">Loading font…</p>
<label for="input">Your text</label><textarea id="input" spellcheck="false"></textarea>
<fieldset><legend>Preview</legend><label>Size <input id="size" type="range" min="12" max="144" value="50"><span id="sizeValue"></span></label><label>Leading <input id="leading" type="range" min="1" max="2" step="0.05" value="1.25"></label><label>Tracking <input id="tracking" type="range" min="0" max="12" step="0.25" value="0"></label><label><input id="dark" type="checkbox">Dark surface</label><button type="button" id="reset">Reset sample</button></fieldset>
<p id="missing" role="status"></p><output id="preview" aria-live="polite"></output><h2>All 254 mapped characters</h2><div id="grid" class="grid"></div>
<p>Source geometry, artistic intent, limitations, and licensing are in the parent README.md / DESIGN.md / OFL.txt. The font is embedded locally; no web services are used.</p>
<script>
'use strict';const cfg=__DATA__;const el=id=>document.getElementById(id);const supported=new Set(cfg.coverage);
function fontStyle(node){node.style.fontFamily='"'+cfg.family+'",monospace';node.style.fontStyle=cfg.cssStyle}
function update(){let value=el('input').value;el('preview').textContent=value;el('preview').style.fontSize=el('size').value+'px';el('preview').style.lineHeight=el('leading').value;el('preview').style.letterSpacing=el('tracking').value+'px';el('sizeValue').textContent=el('size').value+'px';document.body.classList.toggle('dark',el('dark').checked);let missing=[...new Set(Array.from(value).map(c=>c.codePointAt(0)).filter(c=>!supported.has(c)&&![9,10,13].includes(c)))];el('missing').textContent=missing.length?'Missing codepoints: '+missing.map(n=>'U+'+n.toString(16).toUpperCase().padStart(4,'0')).join(', '):''}
fontStyle(el('preview'));el('input').value=cfg.sample;
for(const id of ['input','size','leading','tracking','dark'])el(id).addEventListener('input',update);
el('reset').addEventListener('click',()=>{el('input').value=cfg.sample;el('size').value=50;el('leading').value=1.25;el('tracking').value=0;el('dark').checked=false;update()});
for(const cp of cfg.coverage){let cell=document.createElement('div');cell.className='cell';let code=document.createElement('small');code.textContent='U+'+cp.toString(16).toUpperCase().padStart(4,'0');let symbol=document.createElement('b');symbol.textContent=String.fromCodePoint(cp);fontStyle(symbol);cell.append(code,symbol);el('grid').append(cell)}
update();new FontFace(cfg.family,'url('+cfg.url+')',{style:cfg.cssStyle}).load().then(font=>{document.fonts.add(font);el('status').dataset.loaded='true';el('status').textContent='Font loaded: '+cfg.family+' '+cfg.style}).catch(e=>{el('status').dataset.loaded='false';el('status').textContent='FONT LOAD FAILED — keep specimen and fonts directories together; fallback is not the sample font'})
</script></main></body></html>
'''

def tester(p):
    m=p.m
    config={'family':m.FAMILY,'style':m.STYLE,'cssStyle':'oblique' if m.STYLE=='Oblique' else 'normal','sample':'\n'.join(m.SAMPLES),
        'url':'../fonts/'+filename(m)+'.woff2','coverage':sorted(map(ord,COVERAGE))}
    return (HTML.replace('__FAMILY__',html.escape(m.FAMILY)).replace('__STYLE__',html.escape(m.STYLE))
        .replace('__TAGLINE__',html.escape(m.TAGLINE)).replace('__TRIAL__',html.escape(m.TRIAL))
        .replace('__DATA__',json.dumps(config,ensure_ascii=True).replace('</','<\\/')))

def outputs():
    out={};fonts=[]
    for rel in FAMILIES:
        p=Proof(rel);fonts.append(p)
        out[rel+'/specimen/specimen.svg']=specimen(p)
        out[rel+'/specimen/character-map.svg']=character_map(p)
        out[rel+'/specimen/index.html']=tester(p)
    parts=['<rect width="1600" height="2940" fill="#111920"/>',label('FONT PAYLOAD VAULT / THIRD COHORT / 12 ORIGINAL TYPES',50,54,25,'#d4d8dc')]
    for i,p in enumerate(fonts):
        p.reset();m=p.m;y=93+i*225
        parts.append(f'<path d="M50 {y}H1545" stroke="#3a4a53"/>')
        parts.append(label(f'{i+1:02d}  {m.FAMILY}  / {m.STYLE} / {m.MODE}',50,y+33,21,'#bbc7d0'))
        for s,base,size in [(m.FAMILY.upper(),y+112,67),('Aa Gg Qq 0123456789  Il1| 0O',y+175,36)]:
            parts.append(p.text(s,50,base,p.fitted(s,size,1480),'#f7f4eb'))
        p.f.close()
    out['docs/third-cohort-overview.svg']=svg(1600,2940,parts,'Third Cohort, twelve new font designs')
    return out

def main(check=False):
    out=outputs()
    for path,txt in out.items():
        p=ROOT/path
        if check:
            if not p.exists() or p.read_text(encoding='utf-8')!=txt:raise SystemExit('STALE SPECIMEN: '+path)
        else:p.parent.mkdir(parents=True,exist_ok=True);p.write_text(txt,encoding='utf-8')
    print(f'{len(out)} deterministic SVG and browser specimens '+('verified' if check else 'generated'))

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check',action='store_true')
    main(ap.parse_args().check)
