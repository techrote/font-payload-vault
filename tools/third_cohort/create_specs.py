from pathlib import Path
import textwrap,json
ROOT=Path(__file__).resolve().parents[2]
SPECS=[
 dict(slug='tracebar-mono',family='Tracebar Mono',category='cmd-font-container',lineage='trace',mode='trace',mono=True,advance=740,digit=740,stem=67,track=65,margin=38,style='Regular',trial='18–28 px',tagline='A deliberate wire-route alphabet for machine state and terminal text',
     technique='Flat-ended stroked centre lines retain clean turns and open counters. Carefully separated I, l, 1, pipe and slashed zero make identifiers visible without ligatures. The 740-unit constant advance supports tabular alignment and literal character positions.',
     goal='The linework should resemble a tidy wiring diagram and calibrated dial, not a distressed sci-fi overlay. A low-key engineering voice is more useful here than decorative noise.',
     intent='Source listings, numeric instrumentation and long control labels where column positions must remain stable.',
     limit='No bitmap strikes or hinting; at very small point sizes its diagonals may soften. Confusable geometry checks do not establish an empirical transcription-error benefit.',
     patches={'1':'0,6 3,8 3,0|0,0 6,0','l':'2,8 2,1 3,0 5,0','0':'1,0 5,0 6,1 6,7 5,8 1,8 0,7 0,1 1,0|0.6,0.7 5.4,7.3'}),
 dict(slug='bushing-sans',family='Bushing Sans',category='cmd-font-container',lineage='bushing',mode='bush',mono=False,advance=830,digit=650,stem=75,track=115,margin=35,style='Regular',trial='19–30 px',tagline='Quiet oval lettering for instruments, labels and proportional UI copy',
     technique='An independently placed rounded skeleton uses many intermediate curve points and round joins. Proportional advances follow actual width, but every digit receives 650 units. Bowls are broad, with open C/c and wider lowercase m and w; a/i/g are not capital clones.',
     goal='Suggest the concentric grip and even tolerances of a bushing without drawing literal mechanical objects into the text.',
     intent='Instrument interfaces, short paragraphs, control labels and compact numerical summaries that need proportional rather than terminal-cell spacing.',
     limit='No pair kerning or size-specific optical compensation. It is not truly monospaced despite tabular figures; application-specific UI testing remains necessary.',
     patches={'a':'5.7,0 5.7,5|5.7,4 3.9,5 2,5 0.3,3.8 0.4,1 1.8,0 4.1,0 5.7,1.1','I':'0,8 5,8|2.5,8 2.5,0|0,0 5,0'}),
 dict(slug='microslab',family='Microslab',category='cmd-font-container',lineage='micro',mode='slab',mono=True,advance=760,digit=760,stem=82,track=60,margin=38,style='Regular',trial='20–32 px',tagline='A detented, squared-off typewriter grid with selective slab terminals',
     technique='Angular centre lines are drawn independently of the rounded grammar. Square stems receive narrow rectangular serif feet only at explicitly eligible horizontal terminals; diagonals and tight round counters are protected. The zero carries a central dot rather than a slash.',
     goal='Read like a small machined type slug: a hard mechanical register, not a nostalgic pre-existing slab-serif revival.',
     intent='Monospaced calibration tables, terminal panes, machine inventories and printed labels where fixed columns matter.',
     limit='Slabs add density; evaluation at the actual monitor scale is essential. It lacks native Windows GDI validation and optimized raster strikes.',
     patches={'1':'0,6 3,8 3,0|0,0 6,0','l':'2,8 2,0 6,0','0':'1,0 5,0 6,1 6,7 5,8 1,8 0,7 0,1 1,0|3,4 3,4'}),
 dict(slug='nibble-nine',family='Nibble Nine',category='cmd-font-container',lineage='grid',mode='pixel',mono=True,advance=705,digit=705,stem=69,track=75,margin=38,style='Regular',trial='22–40 px',tagline='A hand-entered nine-row terminal alphabet with uncluttered cell rhythm',
     technique='Sixty-two independently hand-written seven-column bitmap masters, each with nine explicit rows, become rectangle outlines with deliberate row and column gutters. Lowercase has its own pixel arrangements; no old font image or GDI raster resources were imported.',
     goal='The material is an embedded controller display observed close-up, with visible cell logic but enough whitespace to avoid a wall of pixels.',
     intent='Low-density readouts and UI mockups that need strongly indexed cells, including ASCII diagnostics at larger sizes.',
     limit='Outlines approximate the original grid and are not embedded pixel strikes. Pixel-exact appearance at arbitrary screen scaling is not claimed.',
     patches={'0':'.###.../#...#../#..##../#.#.#../##..#../#...#../#...#../.###.../.......','l':'.##..../..#..../..#..../..#..../..#..../..#..../..#..../.###.../.......'}),
 dict(slug='torque-plate',family='Torque Plate',category='hot-font-box',lineage='micro',mode='torque',mono=False,advance=915,digit=780,stem=182,track=70,margin=35,style='Regular',trial='40–110 px',tagline='Compact stock-metal capitals and visible mechanical counter spaces',
     technique='The angular mechanical master is rebuilt with radically wider stock and tight bevels; selected round/diagonal glyphs receive a tiny fastening puncture. Genuine lowercase occupies a separate x-height rather than becoming small caps. Advances follow massive outlines.',
     goal='Emulate stamping force and milled machine plates without copying Diecast Relay’s horizontal relief bands or doing a generic stroke-weight conversion.',
     intent='Very short workshop titles, decals, large numeric labels and display treatments at intentionally high contrast.',
     limit='Counters can close at smaller sizes; test actual output. It is optical artwork, not a physical stencil or certified safety-signage font.',
     patches={'R':'0,0 0,8 5,8 6,7 6,5 5,4 0,4|3,4 6,0','A':'0,0 3,8 6,0|0.9,3.2 5.1,3.2'}),
 dict(slug='sling-arc',family='Sling Arc',category='hot-font-box',lineage='bushing',mode='sling',mono=False,advance=940,digit=785,stem=136,track=108,margin=49,style='Oblique',trial='46–120 px',tagline='Oblique tubular curves given forward visual tension',
     technique='The individually drawn rounded grammar gains substantial tubular weight and an explicit 12° geometric shear. The installed OpenType style is Oblique, with matching italic bits and caret metrics; applications need not synthesize a faux slant.',
     goal='A racing strap pulled taut: smooth curves with directional load, not cursive handwriting or a duplicated Ribbon Torque hollow rail.',
     intent='Short forward-leaning titles, workshop posters and product decals. Tabular numbers support aligned large counters.',
     limit='Large rounded overshoots and open spacing are intentional; fine punctuation need not resemble a continuous tube. It is not qualified for flowing body copy.',
     patches={'S':'5.8,7.3 4.6,8.1 2.1,8.1 0.6,6.8 1.1,5.1 4.8,3.1 6,1.7 5.1,0.2 3.3,0 1.3,0 0,1','v':'0,5 2.6,0 3.3,0 5.9,5'}),
 dict(slug='swarf-bridge',family='Swarf Bridge',category='hot-font-box',lineage='trace',mode='bridge',mono=False,advance=970,digit=820,stem=129,track=100,margin=48,style='Regular',trial='46–110 px',tagline='Hollow welded bridges drawn around a precise line-routing alphabet',
     technique='The route-line sketch is expanded into massive sections, its exterior seam resolved with Boolean unions, then a slim inner offset removed to create a connected welded-border silhouette. Unlike a thin-stroke enlargement, intersections are resolved before outlining.',
     goal='Make letterforms resemble joined bridge members or tubular frame stock, while leaving the interior negative space active.',
     intent='Wide titles, schematic labels, engraved-looking posters and display wordmarks.',
     limit='The interior seam may be lost in ink spread or small raster images. This is not a toolpath, fabricated load-bearing bridge pattern or certified cut stencil.',
     patches={'M':'0,0 0,8 3,4 6,8 6,0','A':'0,0 3,8 6,0|1.2,2.8 4.8,2.8'}),
 dict(slug='raster-forge',family='Raster Forge',category='hot-font-box',lineage='grid',mode='forge',mono=True,advance=770,digit=770,stem=100,track=67,margin=32,style='Regular',trial='40–105 px',tagline='A joined chunky pixel alphabet with asymmetric extrusion tongues',
     technique='Hand-authored seven-column matrix rows become thick, bevelled tiles. On selected exposed right edges, a shorter block tongue extends toward the next cell. Unioned tiles create dense modular letter bodies rather than dotted halos or an enlarged screenshot.',
     goal='Imagine a robotic foundry extruding molten square sections through a stamping die.',
     intent='Large arcade-industrial banners, splash text, title cards and deliberately blocky numerals.',
     limit='The extrusions are optical, not supported machine extrusion geometry. It remains a scalability-first outline with no size-specific pixel strikes.',
     patches={'A':'.###.../#...#../#...#../#...#../#####../#...#../#...#../#...#../.......','R':'####.../#...#../#...#../####.../#.#..../#..#.../#...#../#....#./.......'}),
 dict(slug='shift-ghost',family='Shift Ghost',category='cachemonic',lineage='trace',mode='ghost',mono=True,advance=785,digit=785,stem=62,track=62,margin=43,style='Regular',trial='42–110 px',tagline='Two slightly displaced imprints of a machine-readable skeleton',
     technique='Independent routed strokes are duplicated into two physically separated offset imprints, with small periodic interruptions controlled by the Unicode codepoint. Both impressions are recorded as real outlines and never flicker at runtime.',
     goal='Represent register misalignment from two passes of an industrial printhead, not a digital blur effect or Cache Rattle scanline tear.',
     intent='Fictional machine transcripts, distressed overprints and short code-shaped exhibition text.',
     limit='Double outlines can make 0/O and I/l harder to interpret than the practical Tracebar; not for operational alerts, passwords or safety text.',
     patches={'0':'1,0 5,0 6,1 6,7 5,8 1,8 0,7 0,1 1,0|1,2 5,6','g':'6,5 6,-1 5,-2 1,-2|6,4 4,5 1,5 0,4 0,1 1,0 4,0 6,1'}),
 dict(slug='eddy-notch',family='Eddy Notch',category='cachemonic',lineage='bushing',mode='eddy',mono=False,advance=900,digit=785,stem=144,track=95,margin=46,style='Regular',trial='45–120 px',tagline='Soft, heavy lettering interrupted by deterministic micro-drill voids',
     technique='A new thick rounded outline is drilled at two SHA-256 selected interior coordinates per ASCII glyph. The holes have fixed radius and stable positions; glyph identity never depends on runtime state or the Python random seed.',
     goal='Invoke eddy-current inspection: a smooth casting disclosing tiny nonuniform voids, intentionally distinct from simple distressed typography.',
     intent='Short speculative instrumentation titles and imperfect-device identity marks.',
     limit='The notches are not readable data and do not simulate measured metal flaws. Composed accents and auxiliary symbols retain the neutral recipes and may be visually cleaner.',
     patches={'e':'0.3,2 5.8,2 5.7,3.5 4.5,5 2,5.1 0.5,3.9 0.2,1.5 1.4,0 4.3,0 5.6,0.8','G':'6,6.6 4.7,8 2,8.2 0.5,7 0,4 0.5,1 2,0 5,0 6,1.4 6,3.7 3.3,3.7'}),
 dict(slug='carbon-check',family='Carbon Check',category='cachemonic',lineage='micro',mode='carbon',mono=False,advance=920,digit=790,stem=151,track=96,margin=46,style='Regular',trial='44–120 px',tagline='Massive angled serif material cut by three controlled chatter marks',
     technique='New mechanical letter bodies grow from independently drawn angular contours. SHA-256 determines three bounded diagonal scratch positions, which are subtracted as true negative polygons rather than applied as photographic texture.',
     goal='An industrial inspection print containing scars where the cut collided with the stock; geometric subtraction remains inspectable.',
     intent='Hazard-fiction covers, machine-brand graphics and other intentionally imperfect display text.',
     limit='Artifacts and darker strokes can close apertures at small sizes; scratches have no engineering stress significance. Not a physical material defect model.',
     patches={'S':'6,8 1,8 0,7 0,5 6,3 6,1 5,0 0,0','W':'0,8 1,0 3,5 5,0 6,8'}),
 dict(slug='checksum-haze',family='Checksum Haze',category='cachemonic',lineage='grid',mode='haze',mono=True,advance=785,digit=785,stem=66,track=80,margin=46,style='Regular',trial='48–130 px',tagline='Sparse seven-column pixel emitters with repeatable byte-conditioned satellite dust',
     technique='Each lit bitmap cell becomes a small solid square. SHA-256 of its row pattern/column determines separate neighboring satellites and rare below-row debris. No halo rings, alpha transparency, animation or seeded font substitution is used.',
     goal='Look like faint readback noise around a solid digital bit, not Anode Bloom’s symmetric photometric halo.',
     intent='Fictional corrupted-memory headers, signal-art covers and deliberate digital patina.',
     limit='Small satellites vanish in downsampling. It is not error-correcting code, a physical sensor model or suitable for important serial/credential transcription.',
     patches={'0':'.###.../#...#../#..##../#.#.#../##..#../#...#../#...#../.###.../.......','e':'......./......./.###.../#...#../#####../#....../#...#../.###.../.......'}),
]

for s in SPECS:
    rel=Path(s['category'])/s['slug']; target=ROOT/rel/'source';target.mkdir(parents=True,exist_ok=True)
    shape=(f'"""Original {s["family"]} construction metadata and letter-level overrides.\n'
           f'Core {s["lineage"]} alphabet in tools/third_cohort/masters.py; no source font imported.\n"""\n')
    codes={
    'FAMILY':s['family'],'SLUG':s['slug'],'CATEGORY':s['category'],'LINEAGE':s['lineage'],'MODE':s['mode'],
    'MONO':s['mono'],'ADVANCE':s['advance'],'DIGIT_ADVANCE':s['digit'],'STEM':s['stem'],'TRACK':s['track'],
    'MARGIN':s['margin'],'STYLE':s['style'],'TRIAL':s['trial'],'TAGLINE':s['tagline'],
    'PATCHES':s['patches'],
    }
    lines=['"""Original design metadata and glyph-specific redrawing for '+s['family']+'.','Full editable lineage alphabet: tools/third_cohort/masters.py','"""']
    for k,v in codes.items():lines.append(k+' = '+repr(v))
    lines.append('SAMPLES = '+repr([s['family'].upper(),'Aa Bb Gg Qq 0123456789 Il1| O0','The quick brown fox jumps over the lazy dog.']))
    (target/'design.py').write_text('\n'.join(lines)+'\n')
    # Build family-specific artistic and ergonomic documentation; source traceability central.
    md=f'''# {s['family']} — design / construction record

## Artistic brief

**{s['tagline']}.** This typeface belongs to [`{s['category']}/`](../), the vault's {'terminal and system-interface' if s['category']=='cmd-font-container' else 'workshop display' if s['category']=='hot-font-box' else 'deliberately exploratory'} compartment.

{s['goal']}

## How it is made

{s['technique']}

The editable **family configuration and deliberate glyph corrections** are in [`source/design.py`](source/design.py). The full independently drawn **{s['lineage']} lettering lineage** lives in [`tools/third_cohort/masters.py`](../../tools/third_cohort/masters.py), alongside three other original alphabets. Each lineage has independently authored uppercase, genuine lowercase and ten numerals. Three named faces in this cohort share each base alphabet but use separate construction algorithms and local glyph overrides: **they are distinct typeface treatments, not twelve unrelated hand-drawn alphabets**. Shared new ASCII punctuation and auxiliary recipes are identified in the central workflow; no older vault font is traced or transformed.

The {s['mode']} mode has a nominal primary feature width of **{s['stem']} font units**, an initial advance limit of **{s['advance']} units**, and {'fixed pitch across all codepoints' if s['mono'] else f'proportional text advances with {s["digit"]}-unit tabular digits'}. The style metadata is **{s['style']}**, with a 1000-unit em and 1000/−250 ascent/descent line metrics. All contours are serialized deterministically to integer TrueType coordinates; curves are sampled into polygon segments. There are no imported artwork paths, raster screenshots or proprietary font dependencies.

## Ergonomic or utilitarian intent

{s['intent']} Suggested first trial: **{s['trial']}**. This is a design intention, **not measured reading-speed, fatigue, dyslexia, error-rate or accessibility performance**.

The identity of common `I/l/1/|`, `O/0`, `B/8`, `g/q` groupings and accented letters can be inspected in the full 254-codepoint map and editable local type tester. Some display and experimental faces deliberately trade those distinctions for a specific texture, so their suitability must be judged at actual output resolution and in context.

## Limits, reuse, next work

{s['limit']}

Each 1.000 release has one named style (no variable axes), **254 encoded codepoints and 255 glyph records including `.notdef`**, and ships as a standard TTF and WOFF2. Unicode scope: printable ASCII, Latin-1, selected Windows-1252 characters, arrows, arithmetic marks, light box-drawing and blocks. Precomposed accents are assembled from this design's bodies; some supporting neutral symbols are shared across the twelve fonts. General non-Latin scripts, arbitrary combining sequences, Nerd Fonts and Powerline glyphs are not provided.

There are no native hinting instructions, embedded bitmap strikes, kerning or ligature shaping in version 1.000. Browser testing is limited to hosted Chromium; native Windows GDI/DirectWrite/ClearType behavior and physical-pixel use have not been accepted. No stencil, fabrication or safety-signage qualification is asserted. Rebuild using the root workflow, and inspect visual/functional changes before publishing another version. The new source, binaries and documentation are under **SIL OFL 1.1**; this does not change any earlier vault licensing.
'''
    md=md.replace('../../tools/third_cohort/masters.py','../../tools/third_cohort/masters.py')
    (ROOT/rel/'DESIGN.md').write_text(md)
    readme=f'''# {s['family']}

{s['tagline']}.

**Category:** `{s['category']}` · **{s['style']}** · **{'monospaced' if s['mono'] else 'proportional'}** · trial **{s['trial']}** · **SIL OFL 1.1**.

- Install `fonts/{s['family'].replace(' ','')}-{s['style']}.ttf`; for web use the adjacent `.woff2`.
- `source/design.py`: this face's settings and glyph-level design changes.
- [`DESIGN.md`](DESIGN.md): construction, artistic goals, utility and exclusions.
- [`specimen/specimen.svg`](specimen/specimen.svg): entire alphabet and useful mixed text.
- [`specimen/character-map.svg`](specimen/character-map.svg): all 254 encoded characters.
- [`specimen/index.html`](specimen/index.html): offline type tester (open from a local clone/download).
- [`OFL.txt`](OFL.txt): licensing for this newly created font software.

The full handwritten {s['lineage']} master is held in [`tools/third_cohort/masters.py`](../../tools/third_cohort/masters.py). These twelve designs share four **original** drawn alphabet lineages; each face applies its documented separate outline grammar. See the [shared build and verification workflow](../../docs/THIRD-COHORT-WORKFLOW.md). No copied commercial font outlines or existing vault master files are used.

Rebuild from the repository root:

```sh
python -m pip install -r requirements-third-cohort.txt
python tools/third_cohort/build.py
python tools/third_cohort/verify.py
python tools/third_cohort/specimen.py
```

The font is a first-edition, unhinted outline, not a verified Windows bitmap font. Suggested sizes are trial targets rather than tested human-factors performance.
'''
    (ROOT/rel/'README.md').write_text(readme)

(ROOT/'docs'/'third-cohort-specs.json').write_text(json.dumps([{k:v for k,v in s.items() if k!='patches'} for s in SPECS],indent=2)+'\n')
print('Generated',len(SPECS),'font-specific design/source folders')
