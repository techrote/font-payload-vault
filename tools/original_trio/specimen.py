#!/usr/bin/env python3
"""Font-independent SVG proofs and an offline, no-tracking HTML type tester.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
SVG letterforms are paths from the original master, not embedded font data.
"""
from __future__ import annotations
import argparse
import html
import json
from pathlib import Path
import tempfile
from build import ROOT, FAMILIES, master
from geometry import svg_path
from repertoire import extend, COVERAGE

PAPER='#f3f0e8'; INK='#172829'; MUTED='#526667'; ACCENT='#b84422'
BLURBS=[
 ('PRECISION / TERMINAL','State stays readable.', '640-unit cells / 72-unit strokes / genuine lowercase'),
 ('MASS / DISPLAY','STAMPED NOT POLISHED', 'Chamfered dies / relief slots / capitals + small capitals'),
 ('INTERFERENCE / EXPERIMENT','CACHE MISBEHAVING', 'Independent pixel master / fixed row drift / no animation'),
]


def start(width,height,title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title,quote=True)}">',
            f'<title>{html.escape(title)}</title><rect width="100%" height="100%" fill="{PAPER}"/>']


def label(out,text,x,y,size=15,fill=MUTED):
    out.append(f'<text x="{x}" y="{y}" font-family="system-ui, sans-serif" font-size="{size}" fill="{fill}">{html.escape(text)}</text>')


def text(out,shapes,value,x,y,size,fill=INK,max_width=None):
    width=sum(shapes[c][1] for c in value)*size/1000
    if max_width and width>max_width:size*=max_width/width
    pen=x
    for c in value:
        g,a=shapes[c]
        if not g.is_empty:
            out.append(f'<path d="{svg_path(g)}" transform="translate({pen:.4f} {y}) scale({size/1000:.6f} {-size/1000:.6f})" fill="{fill}"/>')
        pen+=a*size/1000


def write(path,lines):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text('\n'.join(lines)+('\n' if lines[-1].endswith('>') else ''),encoding='utf-8')


def proof(mod,shapes,index):
    out=start(1400,940,mod.FAMILY+' specimen')
    kicker,headline,sub=BLURBS[index]
    label(out,'FONT PAYLOAD VAULT   /   ORIGINAL TRIO 01',50,44)
    label(out,kicker,50,83,17,ACCENT)
    text(out,shapes,mod.FAMILY,45,196,96,max_width=1300)
    label(out,sub,50,243,18)
    out.append(f'<rect x="0" y="277" width="1400" height="196" fill="{INK}"/>')
    text(out,shapes,headline,48,370,72,fill=PAPER,max_width=1300)
    text(out,shapes,'0123456789  /  Il1| O0 gq S5',50,429,34,fill=PAPER)
    for y,line in [(551,'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),(615,'abcdefghijklmnopqrstuvwxyz'),(678,'Sphinx of black quartz, judge my vow.')]:
        text(out,shapes,line,50,y,47,max_width=1290)
    text(out,shapes,'ÀÉÎÖÜ ÇÑ ß æ œ ø  £€¥  ±×÷  ←↑→↓',50,740,34,max_width=1280)
    text(out,shapes,'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~',50,793,32,max_width=1280)
    label(out,'254 Unicode characters / 255 glyphs including .notdef / TTF + WOFF2 / version 1.000',50,853,17)
    label(out,'Unhinted outlines. Size ranges are design targets, not certified readability claims. See DESIGN.md.',50,891,15)
    out.append('</svg>');return out


def chart(mod,shapes):
    rows=(len(shapes)+15)//16
    out=start(1440,140+rows*98,mod.FAMILY+' complete character map')
    label(out,mod.FAMILY+' / COMPLETE ENCODED REPERTOIRE',30,40,24,INK)
    label(out,'Unicode scalar labels identify actual mappings. Spaces are deliberately blank; there are no control-code aliases.',30,76)
    for i,c in enumerate(sorted(shapes)):
        x=24+(i%16)*87;y=140+(i//16)*98
        text(out,shapes,c,x+9,y,42)
        label(out,f'U+{ord(c):04X}',x,y+25,11)
    out.append('</svg>');return out


def tester(mod,index):
    _,headline,_=BLURBS[index]
    stem=mod.FAMILY.replace(' ','')+'-Regular'
    default=24 if index==0 else (56 if index==1 else 42)
    repertoire=''.join(sorted(COVERAGE))
    sample=headline+'\nSphinx of black quartz, judge my vow.\nIl1| O0 gq rn m 0123456789\n£42.00  ±0.25  node_01 != null → [OK]'
    return [f'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{mod.FAMILY} — offline type tester</title>
<style>
@font-face{{font-family:Proof;src:url('../fonts/{stem}.woff2') format('woff2'),url('../fonts/{stem}.ttf') format('truetype');font-weight:400;font-style:normal;font-display:swap;}}
:root{{color-scheme:light dark;--paper:#f3f0e8;--ink:#172829;--line:#abb7b3}}
body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,sans-serif}}
main{{max-width:1240px;margin:auto;padding:24px}}
h1{{font-size:26px}} a{{color:inherit}} .panel{{border:1px solid var(--line);padding:20px;margin:20px 0}}
.controls{{display:flex;gap:20px;flex-wrap:wrap}} label{{display:block}} textarea{{width:100%;box-sizing:border-box;min-height:150px;font:17px/1.6 ui-monospace,monospace;padding:12px;background:var(--paper);color:var(--ink)}}
#proof,.font{{font-family:Proof,monospace;font-weight:400;font-synthesis:none;font-variant-ligatures:none;overflow-wrap:anywhere}}
#proof{{white-space:pre-wrap;font-size:{default}px;line-height:1.25;min-height:240px}}
.font{{font-size:28px;letter-spacing:0}} #coverage{{display:grid;grid-template-columns:repeat(auto-fill,minmax(74px,1fr));gap:8px}} .cell{{text-align:center;padding:8px;border:1px solid var(--line)}} .cp{{font:11px system-ui,sans-serif}} #status{{font-weight:600}} .warning{{font-size:14px;max-width:95ch}}
body.dark{{--paper:#172829;--ink:#f3f0e8;--line:#647775}}
button,input{{font:inherit}} summary{{cursor:pointer}} @media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto}}}}
</style>
<main><p>FONT PAYLOAD VAULT / ORIGINAL TRIO 01</p><h1>{mod.FAMILY}</h1>
<p><a href="../README.md">Readme</a> · <a href="../DESIGN.md">Design &amp; limitations</a> · <a href="specimen.svg">Static proof</a> · <a href="character-map.svg">Character map</a></p>
<p id="status" role="status">Loading local font…</p>
<div class="controls"><label>Size <output id="sizeValue">{default}</output> px<br><input id="size" type="range" min="12" max="112" value="{default}"></label>
<label>Line height <output id="lineValue">1.25</output><br><input id="line" type="range" min="100" max="190" value="125"></label>
<label>Tracking <output id="trackValue">0</output> em<br><input id="track" type="range" min="0" max="15" value="0"></label>
<label><input id="kern" type="checkbox" checked> Kerning</label><button id="polarity" type="button">Invert polarity</button></div>
<label for="input">Your text (text stays in this page; no analytics or storage)</label>
<textarea id="input" spellcheck="false">{html.escape(sample)}</textarea>
<p id="missing" class="warning" role="status"></p><div id="proof" class="panel" aria-live="polite"></div>
<p class="warning">No measured accessibility or fatigue benefit is claimed. Latchline Mono targets readable technical text; Diecast Relay and Cache Rattle are display experiments. These are unhinted outlines, not hand-tuned bitmap strikes. Unsupported characters use your system fallback. Decomposed accents are unsupported; NFC text is required.</p>
<details><summary>All 254 encoded characters</summary><div id="coverage"></div></details></main>
<script>
'use strict';
const supported = new Set(Array.from({json.dumps(repertoire,ensure_ascii=True)}));
const $ = id => document.getElementById(id);
function update() {{
  const value=$('input').value;
  $('proof').textContent=value;
  $('proof').style.fontSize=$('size').value+'px';
  $('proof').style.lineHeight=Number($('line').value)/100;
  $('proof').style.letterSpacing=Number($('track').value)/100+'em';
  $('proof').style.fontKerning=$('kern').checked?'normal':'none';
  $('sizeValue').value=$('size').value;
  $('lineValue').value=(Number($('line').value)/100).toFixed(2);
  $('trackValue').value=(Number($('track').value)/100).toFixed(2);
  const missing=[...new Set(Array.from(value).filter(c=>!supported.has(c)&&!['\\n','\\r','\\t'].includes(c)))];
  $('missing').textContent=missing.length?'Fallback characters: '+missing.map(c=>'U+'+c.codePointAt(0).toString(16).toUpperCase().padStart(4,'0')+' '+c).join(' · '):'All non-control characters in this sample are encoded in this font.';
}}
for(const id of ['input','size','line','track','kern']) $(id).addEventListener('input',update);
$('polarity').addEventListener('click',()=>document.body.classList.toggle('dark'));
for(const c of supported) {{
  const cell=document.createElement('div');cell.className='cell';
  const glyph=document.createElement('div');glyph.className='font';glyph.textContent=c;
  const cp=document.createElement('div');cp.className='cp';cp.textContent='U+'+c.codePointAt(0).toString(16).toUpperCase().padStart(4,'0');
  cell.append(glyph,cp);$('coverage').append(cell);
}}
update();
document.fonts.load('24px Proof','Ag0123').then(faces=>{{
  if(!faces.length)throw new Error('No local font face loaded');
  $('status').textContent='Local {mod.FAMILY} loaded. Nothing is sent off this page.';
}}).catch(()=>{{$('status').textContent='FONT NOT LOADED — displaying fallback. Keep this page beside ../fonts, or serve the repository locally.';}});
</script></html>''']


def generate(output=ROOT):
    overview=start(1400,1120,'Original Trio — Latchline Mono, Diecast Relay and Cache Rattle')
    label(overview,'FONT PAYLOAD VAULT  /  THREE ORIGINAL TYPEFACES',50,44,20,INK)
    label(overview,'One terminal instrument. One cast-metal headline. One corrupted signal.',50,78,18)
    for i,relative in enumerate(FAMILIES):
        mod=master(ROOT/relative);shapes=extend(mod.draw(),mod.STEM,mod.ADVANCE)
        dest=Path(output)/relative/'specimen'
        write(dest/'specimen.svg',proof(mod,shapes,i));write(dest/'character-map.svg',chart(mod,shapes))
        write(dest/'index.html',tester(mod,i))
        y=155+i*303
        label(overview,f'0{i+1}  /  '+BLURBS[i][0],50,y,17,ACCENT)
        text(overview,shapes,mod.FAMILY,45,y+94,92,max_width=1300)
        text(overview,shapes,BLURBS[i][1],50,y+161,42,max_width=1290)
        text(overview,shapes,'0123456789  /  Aa Bb Gg Qq  /  Il1| O0',50,y+220,30,max_width=1290)
        label(overview,BLURBS[i][2],50,y+263,16)
    label(overview,'Version 1.000 • 254 characters each • Built from original geometry, not modified existing fonts.',50,1090,17)
    overview.append('</svg>');write(Path(output)/'docs/original-trio-overview.svg',overview)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='fail on stale or missing checked-in specimens')
    args=parser.parse_args()
    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            generate(Path(tmp))
            for p in Path(tmp).rglob('*'):
                if p.is_file():
                    actual=ROOT/p.relative_to(tmp)
                    if not actual.exists() or actual.read_bytes()!=p.read_bytes():
                        raise SystemExit(f'Stale specimen: {actual.relative_to(ROOT)}; run specimen.py')
        print('All 10 specimen outputs match their sources.')
    else:
        generate();print('Wrote SVG proofs, character maps, offline testers and overview.')
