#!/usr/bin/env python3
"""Fourth Cohort: build the three families and write their proofs.

Reuses the Original Trio serializer, repertoire extension and geometry without
changing the Original Trio family list, manifest or verification suite.
Run from the repository root:  python tools/fourth_cohort/cohort.py
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools' / 'original_trio'))

import build as trio  # noqa: E402  (original_trio serializer, used read-only)
from geometry import svg_path, translate  # noqa: E402
from repertoire import extend  # noqa: E402

FAMILIES = (
    'cmd-font-container/gasket-sans',
    'hot-font-box/ratchet-block',
    'cachemonic/phase-drift',
)
VERSION = '1.100'
COHORT = 'FOURTH COHORT 04'
MANIFEST = 'fourth-cohort-manifest.json'
trio.VERSION = VERSION  # name table and uniqueFontIdentifier
INK, PAPER, MUTED = '#15171a', '#f7f5ef', '#5d6168'
SAMPLES = ['ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz', '0123456789 !?&@#%$*+=-/()']


def lift_into_metrics(g):
    # Shared composites (for example a cedilla under a heavy C) can drop past the
    # declared -250 descender; lift them the minimum distance back inside.
    if not g.is_empty and g.bounds[1] < -250:
        g = translate(g, yoff=-250 - g.bounds[1])
    return g


def shapes_for(folder):
    mod = trio.master(folder)
    shapes = {c: (lift_into_metrics(g), a) for c, (g, a) in extend(mod.draw(), mod.STEM, mod.ADVANCE).items()}
    return mod, shapes


def build_fonts(output_root: Path = ROOT) -> list[dict]:
    info = []
    for relative in FAMILIES:
        mod, shapes = shapes_for(ROOT / relative)
        font = trio.make_font(mod, shapes)
        font['head'].fontRevision = float(VERSION)
        out = output_root / relative / 'fonts'
        out.mkdir(parents=True, exist_ok=True)
        stem = mod.FAMILY.replace(' ', '') + '-Regular'
        files = {}
        for ext, flavor in [('ttf', None), ('woff2', 'woff2')]:
            font.flavor = flavor
            target = out / (stem + '.' + ext)
            font.save(target)
            files[target.relative_to(output_root).as_posix()] = {
                'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
                'bytes': target.stat().st_size,
            }
        info.append({'family': mod.FAMILY, 'version': VERSION, 'codepoints': len(shapes),
                     'glyphs': len(shapes) + 1, 'fixed_pitch': mod.MONO, 'files': files})
        print(f'{mod.FAMILY}: {len(shapes)} characters; TTF + WOFF2')
    manifest = output_root / 'docs' / MANIFEST
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps({'schema': 1, 'families': info}, indent=2) + '\n', encoding='utf-8')
    return info


def draw_text(out, shapes, value, x, y, size):
    pen = x
    for c in value:
        g, a = shapes[c]
        if not g.is_empty:
            out.append(f'<path d="{svg_path(g)}" transform="translate({pen:.4f} {y}) scale({size/1000:.6f} {-size/1000:.6f})" fill="{INK}"/>')
        pen += a * size / 1000


def svg_open(w, h, title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(title, quote=True)}">',
            f'<title>{html.escape(title)}</title><rect width="100%" height="100%" fill="{PAPER}"/>']


def specimen_svg(mod, shapes):
    out = svg_open(1400, 500, mod.FAMILY + ' specimen')
    for i, line in enumerate(SAMPLES):
        draw_text(out, shapes, line, 45, 150 + i * 120, 96 if i < 2 else 80)
    out.append(f'<text x="50" y="460" font-family="system-ui, sans-serif" font-size="15" fill="{MUTED}">{html.escape(mod.FAMILY)} · Version {VERSION} · 254 encoded characters · SIL OFL 1.1 · outline proof, not a readability claim</text>')
    out.append('</svg>')
    return '\n'.join(out) + '\n'


def charmap_svg(mod, shapes):
    chars = sorted(shapes, key=ord)
    cols, cell = 16, 80
    rows = (len(chars) + cols - 1) // cols
    out = svg_open(cols * cell + 60, 110 + rows * cell, mod.FAMILY + ' complete character map')
    out.append(f'<text x="30" y="50" font-family="system-ui, sans-serif" font-size="22" fill="{INK}">{html.escape(mod.FAMILY.upper())} / COMPLETE ENCODED REPERTOIRE</text>')
    for i, c in enumerate(chars):
        x = 30 + (i % cols) * cell
        y = 90 + (i // cols) * cell
        g, _ = shapes[c]
        if not g.is_empty:
            s = 40 / 1000
            out.append(f'<path d="{svg_path(g)}" transform="translate({x+8} {y+52}) scale({s:.6f} {-s:.6f})" fill="{INK}"/>')
        out.append(f'<text x="{x+cell-6}" y="{y+14}" text-anchor="end" font-family="system-ui, sans-serif" font-size="10" fill="{MUTED}">U+{ord(c):04X}</text>')
    out.append('</svg>')
    return '\n'.join(out) + '\n'


def tester_html(mod, shapes):
    stem = mod.FAMILY.replace(' ', '') + '-Regular'
    supported = json.dumps(''.join(sorted(shapes, key=ord)))
    name = html.escape(mod.FAMILY)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} — offline type tester</title>
<style>
@font-face {{ font-family: "{name}"; src: url("../fonts/{stem}.woff2") format("woff2"); }}
:root {{ color-scheme: light dark; --ink:{INK}; --paper:{PAPER}; --muted:{MUTED}; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --ink:#ecebe6; --paper:#17191c; --muted:#a3a7ae; }} }}
:root[data-theme="dark"] {{ --ink:#ecebe6; --paper:#17191c; --muted:#a3a7ae; }}
body {{ margin:0; background:var(--paper); color:var(--ink); font:16px/1.5 system-ui, sans-serif; }}
main {{ max-width:960px; margin:0 auto; padding:16px; }}
textarea {{ width:100%; box-sizing:border-box; font:inherit; min-height:5em; background:transparent; color:var(--ink); border:1px solid var(--muted); padding:8px; }}
#sample {{ font-family:"{name}", monospace; white-space:pre-wrap; overflow-wrap:anywhere; margin:16px 0; }}
label {{ display:block; margin:8px 0; }}
#status {{ color:var(--muted); font-size:14px; }}
</style></head>
<body><main>
<p>FONT PAYLOAD VAULT / {COHORT}</p>
<h1>{name}</h1>
<p>Local font only. Nothing is sent off this page.</p>
<label>Text <textarea id="input" spellcheck="false">{name}
ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !?&amp;@#%</textarea></label>
<label>Size <input id="size" type="range" min="16" max="120" value="48"> <span id="sizeOut">48</span>px</label>
<div id="sample"></div>
<p id="status"></p>
</main>
<script>
const SUPPORTED = new Set({supported});
const $ = id => document.getElementById(id);
const sample = $('sample'), input = $('input'), size = $('size'), status = $('status');
function render() {{
  sample.textContent = input.value;
  sample.style.fontSize = size.value + 'px';
  $('sizeOut').textContent = size.value;
  const missing = [...new Set([...input.value].filter(c => c.codePointAt(0) > 32 && !SUPPORTED.has(c)))];
  status.textContent = missing.length ? 'Not in this font: ' + missing.join(' ') : 'All characters are in this font.';
}}
input.addEventListener('input', render); size.addEventListener('input', render);
document.fonts.load('48px "{name}"').then(render, () => {{ status.textContent = 'Font failed to load; text is shown in fallback type.'; render(); }});
render();
</script></body></html>
"""


def build_proofs(output_root: Path = ROOT) -> None:
    for relative in FAMILIES:
        mod, shapes = shapes_for(ROOT / relative)
        target = output_root / relative / 'specimen'
        target.mkdir(parents=True, exist_ok=True)
        (target / 'specimen.svg').write_text(specimen_svg(mod, shapes), encoding='utf-8')
        (target / 'character-map.svg').write_text(charmap_svg(mod, shapes), encoding='utf-8')
        (target / 'index.html').write_text(tester_html(mod, shapes), encoding='utf-8')
        print(f'{mod.FAMILY}: proofs written')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT, help='output root (sources stay unchanged)')
    parser.add_argument('--proofs-only', action='store_true')
    args = parser.parse_args()
    root = args.output.resolve()
    if not args.proofs_only:
        build_fonts(root)
    build_proofs(root)
