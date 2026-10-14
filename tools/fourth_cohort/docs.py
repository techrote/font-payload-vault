#!/usr/bin/env python3
"""Reproducible per-family documentation, licence copies and cohort reference.
Copyright (c) 2026 techrote. SIL OFL 1.1; see OFL.txt.
"""
from __future__ import annotations
import argparse
from build import ROOT,FAMILIES,config,filename

DETAILS = {
'Railkey Mono': (
'''Railkey Mono is the practical end of the new rail lineage. The starting image
is a bank of latched terminals: straight channels, folded shoulders and a fixed
register. It is not a redraw of Tracebar or Latchline; its 62 letter/figure paths
were entered independently in `masters/rail.py`. Capital A has a short flat apex,
C has long vertical sides, and the g descender returns beneath the body rather
than copying q. Narrow letters are drawn to occupy a full terminal cell.''',
'''The original M/L/Z skeletons are expanded with a 78-by-78-unit nib, flat caps
and bevel joins. Horizontal placement is normalized into 680-unit advances;
wide m/w remain within their cells. There are no random cuts, layout ligatures
or kerning. The same new skeleton also supports Flange Banner, whose broader
nib and attached tabs are a different display treatment, not a second hidden
master. Railkey keeps those tabs out of practical text.''',
'''The intended trial is source listings, tabular diagnostics and instrument
labels. Barred I, flagged 1, an exiting l and a taller plain pipe supply distinct
shape cues. Zero has its own narrower loop and a slash, not an O alias. Fixed
advances preserve literal columns; that is a geometry property, not a claim of
fewer transcription errors. Wide tracking and comparatively squared lowercase
are deliberate costs. Test terminal fallback and the actual size before use.'''),
'Gimbal Sans': (
'''Gimbal Sans offers a proportional, comparatively quiet answer to the vault's
instrument theme. The gimbal metaphor is articulation rather than rigidity:
open curves, noncircular shoulders, varied widths and a measured stroke contrast.
Its new GIMBAL path set is not the Bushing or Collet alphabet. Capitals and real
lowercase were authored separately, with wider m/w and narrower i/l/r.''',
'''A 76-by-68-unit elliptical nib expands the sampled original cubic paths. The
unequal axes give verticals slightly more mass than horizontals. Bowls are
resolved from complete paths, and overlaps are united before integer contour
export. Letter advance follows the actual ink span plus bearings; figures share
650 units. The related Orbit Hatch uses the same newly drawn paths with a much
heavier body and explicit perimeter-plus-hatching construction.''',
'''The use hypothesis is short prose around instruments, menu labels and numeric
readouts. It is not fixed pitch and should not replace a terminal's cell font.
Slashed zero, flagged one and a hooked l aid shape differentiation in short
strings; narrow counter and confusable checks exercise those exact drawings.
There is no kerning program, so AV/To and mixed punctuation still need optical
spacing review. No reading-speed or fatigue benefit has been measured.'''),
'Quoin Serif': (
'''Quoin Serif introduces wedge-serif text into a vault dominated by technical
sans and pixel work. A quoin holds a printing forme; the image here is letters
secured by small wedges. The newly authored Roman skeleton is independent of
the new sans, rail, cursive, facet and grid alphabets. It includes separate
lowercase, an exiting l, a slashed zero and non-identical B/8 construction.''',
'''The positive body is drawn with an anisotropic 90-by-42-unit nib. The apparent
stroke contrast therefore comes from geometry, not a contrast filter on an
existing font. Explicit FEET and TOPS tables select serif attachment sites;
162-unit-wide, 56-unit-high six-vertex wedges appear only there. They are not
added at every node of a curve. Quoin's Broach Black sibling uses 152-by-86
stock and larger wedges; both openly share this new skeleton lineage.''',
'''The intention is short explanatory text, captions and workshop editorial
compositions at a larger trial size than the sans. Wedge terminals give a
horizontal anchoring rhythm while thin cross-strokes keep the texture open.
They can also vanish under reduction or gain too much prominence on coarse
screens. The practical counter tests begin at 24 px, not at tiny menu sizes.
This first version has no kerning, hinting, print trial or prolonged reading
study; such assessments precede claims about body-text suitability.'''),
'Pinfeed Grid': (
'''Pinfeed Grid follows continuous paper-feed machinery rather than another
sparse dot display. Its new eight-column alphabet uses eleven nominal capital
rows; lowercase has four leading blank rows and separately drawn bodies, with
additional descender rows where required. The grids are new source artwork,
not extracts of Knurled Swarf, Nibble Nine, Cache Rattle or an installed font.''',
'''Each filled cell becomes a 60-unit square, and adjacent cells are united into
continuous stock. Eleven rows reach 660 units; the seven-row lowercase body
reaches 420. Every encoded character has a 640-unit advance. The i dot is raised
two units above the shared accent-removal boundary so replacing it cannot leave
a zero-area edge or a residual dot. Punchloom shares this newly entered grid,
but replaces solid cells with explicitly notched over/under modules.''',
'''The intended setting is controller-like labels, short terminal experiments
and fixed-cell diagrams. Continuous blocks provide a denser alternative to
separated emitters. The 8-column width permits separate I/l/1 and a diagonally
marked zero; it also makes m/w quite dense. These are scalable outlines with
no bitmap strikes or pixel-hinting acceptance. “Grid” does not promise a clean
pixel at every font size. Rendering below the stated trial range is inspection,
not a guarantee of practical usability.'''),
'Flange Banner': (
'''Flange Banner moves the rail lineage out of operational text and into broad,
forceful headings. Its reference is an extruded section with attachment tabs,
not distressed paint or a historical factory sign. It intentionally shares the
newly drawn rail skeleton with Railkey Mono, while changing mass, spacing and
the treatment of long verticals. It is not an independently drawn second rail
alphabet, and the provenance does not pretend otherwise.''',
'''The body uses a 140-by-110-unit nib with flat caps and bevel joins. Only
vertical source segments longer than 270 units receive tabs. Two attachment
positions, at 8% and 92% of each qualifying segment, add 206-by-44-unit flanges.
Those positive pieces are united with the body before serialization. Letters
have proportional advances and figures share 800 units. No scanline is removed
and no contour is offset into a fake shadow.''',
'''The purpose is headline hierarchy and material character in short workshop
labels. The long-stem tabs create a different cadence from the quieter mono
without making every corner equally noisy. Dense lowercase, strong bearings
and unkerned capitals cost space. Trial it in real headings before reducing it.
Neither the tab dimensions nor the word “flange” constitutes a fabrication,
physical stencil or safety-signage specification.'''),
'Broach Black': (
'''Broach Black is the dense display counterpart of the new Quoin skeleton. Its
image is a row of cutting teeth: dark vertical mass punctuated by wedge feet.
The inherited skeleton is disclosed, not passed off as a separately authored
alphabet. It differs from the older Torque Plate and Flypress designs through
Roman curve construction, anisotropic stroke mass and individually selected
wedge-serif sites rather than notched mechanical stock.''',
'''A 152-by-86-unit nib replaces Quoin Serif's lighter 90-by-42 nib. The selected
wedge terminals are 184 units wide and 68 high. Original curves and overlays
are resolved as positive area before export; the counters are the remaining
negative regions, not a hollow-font effect. Letter widths follow the ink span;
figures have 760-unit advances. “Black” is part of the family name describing
the artwork. The sole named style is Regular, with weight metadata 400; no
weight family or Bold style-link is claimed.''',
'''The utilitarian intention is visual hierarchy in short titles and prominent
numeric labels. Broad stems should remain visibly heavier than accompanying
text, but dense counters are a reason not to choose it for small interface
text. Review the separate full alphabet and reduced samples, particularly a/e,
B/8 and sequences involving serifs. No distance-legibility, accessibility,
printing or cutting test is implied by the successful font-software checks.'''),
'Camber Script': (
'''Camber Script adds looped cursive movement to the workshop collection. It is
built from a new set of separately drawn capital, lowercase and figure curves.
The long ascender loops in b/h/l and the returning g/y tails are structural
features of those paths, not synthetic italics applied to Gimbal Sans or an
existing font. Adjacent letters remain unconnected: this is not a handwriting
shaping system with contextual joins.''',
'''The new cubic skeletons are sampled at 24 intervals and expanded by a
90-by-58-unit nib. A shear of x += 0.16*y is then applied before fitting into
proportional advances. Figures share 760 units. The installed style is Oblique;
negative italic angle, oblique/italic selection bits, macStyle and caret slope
are consistent with the nominal shear. Horizontal fitting of an unusually
wide glyph can slightly change its effective angle. The Flux Stitch sibling
uses these new curves with genuine arclength gaps instead of a solid nib path.''',
'''The intended use is a short decorative title or a light contrasting line in
a composition dominated by angular lettering. Open spacing makes individual
loops inspectable but does not reproduce the rhythm of connected handwriting.
It has no contextual alternates or pair kerning. Long ascenders and tails
consume line height; reducing them for dense text is not a tested use. Native
Windows, cursive reading performance and physical tube/engraving suitability
remain separate questions, not accepted features of this release.'''),
'Octant Cut': (
'''Octant Cut starts from a new faceted alphabet. The main bowls are elongated
many-sided paths, not rounded sans shapes with a bevel applied afterwards.
Capital A has side walls and a roof; O is a tall faceted loop; lowercase a/e/g
retain their own body structures. This new OCTANT skeleton is independent of
RAIL, even though both use straight segments. Its geometric inscription-like
rhythm is the artistic objective, not a reconstruction of a historical script.''',
'''A 113-by-82-unit anisotropic nib with flat caps and bevel joins expands the
new paths. Proportional advances fit the faceted silhouettes, while figures
share 700 units. Explicitly widened 52-unit i/j dot strokes prevent a flat-cap
one-unit source segment from disappearing into a hairline. Phase Cairn shares
this new skeleton but samples it as separated tangent-aligned stones. That
relationship is intentional and documented.''',
'''The use hypothesis is narrow monumental headings and distinctive short
workshop labels. Facets are meant to survive as a clear silhouette, with real
lowercase available for mixed-case titles. The pointed bowls and compact
counter rhythm are poor grounds for a small body-text recommendation. It has
not been tested as stone carving, laser lettering, an emergency notice or a
manufactured stencil. Review at the reproduction size before relying on it.'''),
'Orbit Hatch': (
'''Orbit Hatch is an engraving experiment using the freshly drawn Gimbal
skeleton, not an effect applied to an older vault font. Its visual contrast is
between a continuous letter boundary and a striped interior: the outline says
stable object, while the interior reads as a material surface. It deliberately
avoids the previous cohort's scanline tearing and displaced ghost imprints.''',
'''The body is first expanded with a heavy 156-by-138-unit nib. An 18-unit inner
inset defines a continuous perimeter band. That band is united with the body
intersected by 12-unit-wide, 45-degree hatch strokes placed at 58-unit horizontal
intervals. The whole construction remains monochrome ordinary contours: there
is no image fill, shader, opacity or runtime randomness. Letter widths are
proportional and figure advances are 740 units. Supporting accent and currency
recipes remain neutral rather than receiving a second hatch treatment.''',
'''The intention is short large headings or fictional instrument artwork with
a repeatable engraved surface. Hatch lines and the narrow perimeter are highly
scale-dependent; low-resolution output can turn them into grey texture. No
measured reading advantage is claimed, and the family is not an operational
alert or transcription face. Neither the hatch spacing nor the inset specifies
a tool diameter or physical engraving process. Composition at the actual
output scale is required before aesthetic acceptance.'''),
'Punchloom': (
'''Punchloom reinterprets the new Pinfeed grid as a woven field. The underlying
letters are intentionally shared with Pinfeed Grid: this is a pair of related
faces with different material treatments, not two independent handwritten
alphabets. The parent grid itself was newly entered for this cohort and has
no copied earlier font cells.''',
'''Each occupied 60-unit cell becomes a skewed quadrilateral with a rectangular
internal slit. The outer primitive has four vertices:
(3,7), (54,1), (59,53), (7,59), relative to the cell origin. Row-plus-column
parity selects a vertical or horizontal 12-unit-wide slit. The alternating
cut direction suggests over/under threads while leaving each cell at its
original position. Neighbouring modules do not grow into an extruded shadow.
Advances remain 640 units and the i-dot boundary fix is shared with Pinfeed.''',
'''The useful constraint is repeatability in fixed-cell decorative layouts.
The woven texture is best assessed at large sizes; small samples are only
robustness checks and may look like uneven grey pixels. It is not a raster-font
strike, knitting instruction, weave simulation or manufacturing pattern.
Auxiliary symbols and accents use the neutral repertoire engine rather than
pretending all Unicode shapes were separately woven. Do not use this face as
the only rendering of alarms, credentials or important numeric identifiers.'''),
'Flux Stitch': (
'''Flux Stitch converts the newly drawn Camber curves into an interrupted,
sewn-line appearance. The curve identity is deliberately shared with Camber
Script, but the distribution of ink follows distance along each path, not
horizontal rows or random erased patches. This makes its gaps bend with loops
and tails instead of imitating a scan timing fault.''',
'''Each separate polyline is divided into a whole number of nominal 150-unit
periods. Within each fitted period, 72/150 of the length receives a 44-unit
round stroke. End caps expand the dashes, so the unpainted interval must exceed
the nib width. An early visual check found a shorter interval closed by those
caps; the corrected straight-line regression requires four separated pieces
and more than 25 units between neighbours. A 0.16 shear creates the real
Oblique style. Punctuation is deliberately solid and supporting symbols stay
neutral; the effect is not claimed for every encoded mark.''',
'''The purpose is light, interrupted decorative titles and fictional textile or
signal-path labels. The gaps must remain visible at the composition size or
the artistic distinction from Camber disappears. That is why the new regression
checks disconnected components rather than just different file hashes. This
is not embroidery, toolpath or stitch-machine output. No ergonomic advantage
or suitability for live diagnostics is claimed; it should not carry important
state or transcription content without a plain-text alternative.'''),
'Phase Cairn': (
'''Phase Cairn takes the newly drawn Octant skeleton apart into small oriented
stones. It is the experimental sibling of Octant Cut, with an explicitly shared
new alphabet. Its reference is a path recovered from separated markers, not a
corrupted file or a shuffled character encoding. Character identity and advance
remain fixed even though the apparent stroke becomes fragmented.''',
'''Each separate source polyline is split into a whole number of intervals with
a nominal 104-unit period. A four-vertex stone is placed at each interval's
midpoint and aligned with the local path tangent. Its longitudinal half-length
is at most 46 units, further limited to 40% of the actual interval; its transverse
half-width is 43 units. The resulting negative gaps are explicit geometry.
All encoded characters retain a 720-unit advance. Widened source dot segments
keep i/j markers substantial rather than degenerate slivers.''',
'''The intended utility is a stable grid for decorative broken inscriptions and
fictional archaeological/electronic graphics. The sparse stones are likely to
lose or change texture when reduced, so the robustness renders do not endorse
them for practical text. There is no seed, temporal animation, substitution or
image-based effect. Accents, arrows and functional box/blocks remain neutral
shared geometry. Important status, alarms and identifiers need a separate
plain rendering; no human-factor or fabrication suitability is inferred.'''),
}

SHARED = '''## Shared repertoire, geometry and limits

This face has **254 mapped codepoints** and 255 glyph records including `.notdef`:
printable ASCII, Latin-1, defined Windows-1252 additions and selected mathematical,
arrow, light box and block symbols. The full character map is the exact inventory.
It does not include generalized combining-mark positioning, arbitrary non-Latin
scripts, Nerd Fonts or Powerline additions. Prefer supported precomposed letters;
unsupported decomposed sequences can invoke fallback.

The letter/digit skeleton is new artwork. ASCII punctuation is new shared
Fourth Cohort construction, not a separate redraw per family. The unchanged
Original Trio `geometry.py` and `repertoire.py` supply Boolean/normalization and
neutral auxiliary recipes based on the current family's own bodies. Thus some
currency, accent and functional symbols intentionally have a more neutral style.
No existing compiled font, installed font or old alphabet master is a design input.

All fonts use a 1000-unit em, 1000/-250 line metrics and no extra line gap. Rounded
curves are sampled into line segments, so the TrueType outlines are polygons,
not native quadratic curves. Quantized outlines are checked against their source.
The finalizer fits only out-of-range nonfunctional glyphs into -242..984, without
clipping ink; every such scale/translation is recorded in the font manifest.
Functional boxes and blocks keep their full logical cell. Application line height,
fallback and raster rounding can nevertheless produce visible seams.

These are unhinted first releases, one style per family. No bitmap strikes,
variable axes, pair kerning or ligature substitutions are present. All trial
sizes and utilitarian aims are hypotheses, not measured improvements in reading
speed, fatigue, dyslexia or accessibility. Native Windows installation and
GDI/DirectWrite/ClearType comparisons, physical display/print tests, distance
legibility and fabrication qualification are not claimed.

## Review, edits and reproduction

See the source recipe, shared new lineage master, full specimen and character
map together. Make intentional changes to the master or recipe, then regenerate
fonts, docs and specimens and rerun the complete qualification. Tests establish
coverage, exact outlines, metrics, sanitizer acceptance, selected practical
confusables/counters, deterministic rebuilds and browser functionality; they do
not replace human assessment of a real composition. Historical successful JSON
records are valid only for their bound font/source manifest.

The new font software and accompanying design documents use the included
**SIL Open Font License 1.1**, with no Reserved Font Names. This does not relicense
older vault content. Full production details: [Fourth Cohort workflow](../../docs/FOURTH-COHORT-WORKFLOW.md).
'''

WORKFLOW = '''# Fourth Cohort / 04 — twelve faces from six new lineages

Inspected base: `5ef683bbc74e7a0d52f41a898b7a44b232b21e40` on `main`.
The previous dozen was already merged; no competing open PR was present.
The category briefs, previous sources/docs and prior specimens informed the
new work. Existing families, masters, archived names and retirement files are
not modified. Only root/category indexes receive additive links.

![Fourth Cohort](fourth-cohort-overview.svg)

## Design register

__TABLE__

## What is independently new

There are **six newly authored 62-character letter/figure masters**, not twelve
independent alphabets: `rail`, `gimbal`, `quoin`, `pinfeed`, `camber`, `octant`.
They are stored as inspectable source in `tools/fourth_cohort/masters/`. Each
supports two openly related family recipes in the individual `source/design.py`
files. The rail/facet paths, open curves, contrast-serif skeleton, looped cursive
and eight-column grid were entered for this cohort, without extracting, tracing,
renaming or filtering any earlier font's letters.

The cohort contributes its own shared ASCII punctuation and treatment engine.
Original Trio's `geometry.py` and `repertoire.py` are reused unchanged for geometry
normalization and neutral auxiliary recipes. Their exact Git blob identities are
regression-checked. This reuse includes some accent/currency/functional shapes;
those are not falsely presented as twelve independently drawn international
repertoires. Master/recipe/compiler/helper SHA-256 values accompany the output
manifest, making the actual dependency boundary inspectable.

The new contribution follows the vault's utilitarian/display/experimental split
but adds serif contrast, genuinely looped cursive, over/under modules, hatching
and arclength fragmentation rather than twelve more scanline variations.

## Geometry and export contract

The UPM is 1000, ascent/descent 1000/-250, and line gap zero. Five continuous
lineage masters use original M/L/C/Z paths; cubics are sampled at 24 intervals.
Nib geometry uses affine circle buffers. The grid master has eight columns,
eleven capital rows and meaningful leading/descender rows in lowercase.
Every final contour is normalized and integer-quantized. TTF and WOFF2 contain
the same unhinted, quadratic-free outlines and deterministic metadata.

All twelve have real lowercase, 254 mapped codepoints and 255 glyph records.
Their cmap is identical in coverage, not in artwork. Railkey Mono, Pinfeed Grid,
Punchloom and Phase Cairn have one advance for every encoded glyph. The other
eight are proportional with tabular figures. Camber Script and Flux Stitch are
real Oblique styles; names, flags, caret slope and negative italic angle agree.
Cap/x-height metadata is tied to H/x ink bounds, not guessed from nominal paths.

ASCII punctuation remains neutral; styled alphabet bodies feed precomposed
accent assembly. Only nonfunctional glyphs that exceed -242..984 are fitted
vertically, never cropped. Those exact fits are listed in the manifest. Box and
block geometry spans the full 1250-unit cell. No kerning, ligatures, variation
axes or bitmap strikes are supplied. Each face-specific DESIGN.md records its
actual nib, treatment, shared lineage, aesthetic intention and use limits.

## Rebuild and inspect

From the repository root, use Python 3.12 and the inherited pinned toolchain:

```sh
python -m pip install -r requirements-fourth-cohort.txt
python tools/fourth_cohort/build.py
python tools/fourth_cohort/docs.py
python tools/fourth_cohort/specimen.py
python tools/fourth_cohort/verify.py
python tools/fourth_cohort/docs.py --check
python tools/fourth_cohort/specimen.py --check
```

For mandatory hosted font/browser acceptance:

```sh
sudo apt-get update
sudo apt-get install -y --no-install-recommends libfreetype6 opentype-sanitizer
python -m playwright install --with-deps chromium
python tools/fourth_cohort/verify.py --require-ots --report docs/fourth-cohort-verification.json
python tools/fourth_cohort/browser_smoke.py --report docs/fourth-cohort-browser-verification.json
python tools/fourth_cohort/verify.py --require-ots --require-records
```

`--output /tmp/fourth-cohort-rebuild` builds to an isolated root. Normal CI does
not rebuild over committed fonts before checking them. `docs.py --check` and
`specimen.py --check` reject stale generated documentation and proofs.
`browser_smoke.py --executable /path/to/chromium` is an optional local override;
hosted acceptance uses Chromium installed by the pinned Playwright package.
A missing local sanitizer can be reported as a skip without `--require-ots`;
that is not hosted acceptance. Environment-blocked browser runs are not passes.

After an intentional source edit, remove the old two success reports before
requalifying, then retain newly produced font and browser records together.
The binding tests deliberately reject successful records for different font or
source bytes. Do not weaken that check to make an old pass survive a new design.

## What qualification establishes

There are **20 test groups**, covering all six master inventories; complete
coverage/nonempty valid area; bounds, pitch and tabular figures; exact serialized
contours/bearings; names/styles/ink heights; output and source manifest binding;
**9,144 paired FreeType renders** at 18/36/68 px; four practical faces' confusable
signatures at 18/24/32 px; enclosed counters at 24/32/40 px; functional tiling;
distinct final alphabets and true lowercase; malformed-source rejection; real
stitch gaps; grid/weave and i-dot geometry; serif/flange/hatch/cairn regressions;
nonclipping vertical fits; unchanged shared helpers; two independent hash-seed
rebuilds; mandatory OTS for all 24 exports; and retained evidence binding.

Selected raster differences/counters are limited engineering assertions, not
proof of reading performance. The parser and geometry regressions protect real
review findings rather than relying on font filenames being different.

The **37 specimen outputs** are a path-based SVG proof, complete character map
and local HTML tester for every face, plus a cohort overview. Lettering is
extracted from the compiled TTF. Proof size-ladder labels use unscaled short
samples so an automatic fit cannot mislabel a reduced sample as a larger size.
Only explanatory SVG labels use a generic UI font.

All twelve testers are checked over loopback HTTP and direct file URLs: actual
family selection, font loading, 254 repertoire cells, literal user text rather
than HTML, missing combining/astral-codepoint warnings, size/leading/tracking,
polarity, full reset and visible failure in a fresh context when the WOFF2 is
blocked. No CDN or external requests are needed. Chromium acceptance is not
universal-browser or Windows-installation acceptance.

## Review findings and publication

Source/visual review widened the Octant i/j dot segments, gave Quoin l an exit,
raised the grid i-dot above the accent-removal boundary, widened stitch gaps
that rounded caps originally closed, tied height metadata to actual ink, and
kept proof ladder text at its labelled size. The corresponding deterministic
regressions are part of the delivered tests.

Only checksummed UTF-8 source text is staged for initial publication on the
dedicated branch. A hosted runner builds the fonts and verifies that its complete
manifest matches the locally reviewed identity, runs mandatory font/browser
qualification, generates docs/proofs and commits the outputs. Temporary source
transport is removed. The write-enabled bootstrap workflow is then replaced
with read-only regression CI before the final PR is reviewed.

Squash merge keeps transport out of main history. Merge only after current-head
CI succeeds; verify the landed main tree and its normal post-merge run without
starting duplicate workflows. The PR discussion records those actual identities.
Retained JSON is historical, source/font-hash-bound evidence, not proof of an
arbitrary later branch head. Source files and existing families remain available
for inspection even when a font is not suitable for a particular user.

## Explicit limits and licence scope

No native Windows installation, GDI/DirectWrite/ClearType comparison, monitor or
print trial, human-factors study, regulated signage test, physical stencil,
engraving, weaving or embroidery qualification is claimed. Decorative geometry
is not a toolpath. Experimental text must not be the sole channel for important
alarms, credentials or transcription. Trial sizes are design contexts, not
certifications or measured accessibility advantages.

New font software, source, proofs and design documents use the accompanying SIL
OFL 1.1 with no Reserved Font Names. Existing families/archive material is not
relicensed. The original helper licences remain in place.

## Technical references

- FontTools official documentation: https://fonttools.readthedocs.io/
- OpenType OS/2 metrics and style flags: https://learn.microsoft.com/en-us/typography/opentype/spec/os2
- Prior production context: [Third Cohort](THIRD-COHORT-WORKFLOW.md) and [Original Trio](ORIGINAL-TRIO-WORKFLOW.md).

These explain formats and tools. Actual new artwork is the source; software
acceptance is the exact manifest and CI evidence, not a tooling citation.
'''


def index_block():
    rows=[]
    for i in range(4):
        parts=[]
        for j in (i,i+4,i+8):
            rel=FAMILIES[j];parts.append('['+config(rel)['family']+']('+rel+'/)')
        rows.append('| '+' | '.join(parts)+' |')
    return ('## Fourth Cohort / 04 — twelve new faces\n\n![Fourth Cohort overview](docs/fourth-cohort-overview.svg)\n\n'
      '| Practical / system | Workshop / display | Experimental |\n|---|---|---|\n'+'\n'.join(rows)+'\n\n'
      'Twelve faces from six newly authored alphabet lineages, with explicit sibling\n'
      'relationships, original sources, TTF + WOFF2, 254 codepoints, design notes,\n'
      'full maps and local testers. Includes new serif, looped cursive, weave, hatch\n'
      'and fragmented-path directions. [Creation, qualification and limits](docs/FOURTH-COHORT-WORKFLOW.md).\n\n')


def outputs():
    out={};rows=[];licence=(ROOT/'tools/original_trio/OFL.txt').read_text(encoding='utf-8')
    for rel in FAMILIES:
        c=config(rel);name=c['family'];brief,construction,utility=DETAILS[name]
        siblings=[config(p)['family'] for p in FAMILIES if config(p)['lineage']==c['lineage'] and p!=rel]
        out[rel+'/DESIGN.md']=(f'# {name} — design and construction\n\n## Artistic brief and lineage\n\n'+brief+'\n\n## Creation technique\n\n'+construction+
          '\n\n## Ergonomic or utilitarian intention\n\n'+utility+
          f"\n\n## Exact first-release settings\n\n| Property | Value |\n|---|---|\n| Style | {c['style']} |\n| Pitch | {'Fixed' if c['mono'] else 'Proportional; tabular digits'} |\n| Figure / default cell | {c['advance']} units |\n| H / x ink height | {c['cap_height']} / {c['x_height']} units |\n| Trial range | {c['trial'][0]}–{c['trial'][1]} px |\n| New shared lineage | `{c['lineage']}`; sibling {siblings[0]} |\n\n"+
          SHARED)
        out[rel+'/README.md']=f'''# {name}

**{c['style']} / version 1.000** — {c['tagline']}

![{name} specimen](specimen/specimen.svg)

## Payload and source

| File | Purpose |
|---|---|
| `fonts/{filename(c)}.ttf` | Desktop TrueType outline font |
| `fonts/{filename(c)}.woff2` | Compressed web font, same drawings and metrics |
| [source/design.py](source/design.py) | Editable family-specific recipe |
| [Shared new master](../../tools/fourth_cohort/masters/{c['lineage']}.py) | Newly authored alphabet/figures used by this lineage's two faces |
| [DESIGN.md](DESIGN.md) | Technique, artistic goal, intended utility and limitations |
| [specimen/index.html](specimen/index.html) | Interactive local tester; preserve adjacent fonts folder |
| [Character map](specimen/character-map.svg) | Exact 254-codepoint inventory |
| [OFL.txt](OFL.txt) | SIL Open Font License 1.1, no Reserved Font Names |

This is one new face, not a multi-weight family. Lowercase is present. The new
`{c['lineage']}` alphabet is shared openly with **{siblings[0]}**; no earlier font's
letters or grids were used as its master. Neutral punctuation/auxiliary recipes
are shared as described in DESIGN.md.

## Use and preview

Install the TTF through the operating system's font installer. Native Windows
installation and rendering have not been accepted in this task. For a preview
without installation, open the local HTML tester from a checkout. GitHub's
source viewer does not execute the tester. It warns on missing characters or
font-load failure rather than silently presenting fallback as this font.

The initial trial range is **{c['trial'][0]}–{c['trial'][1]} px**. This is a design
context, not a claim of measured legibility, comfort or accessibility. Read
DESIGN.md before using a display/experimental face for actual information.
No kerning, ligatures, hinting, bitmap strikes, combining-mark layout or general
non-Latin repertoire is supplied.

```css
@font-face {{
  font-family: "{name}";
  src: url("fonts/{filename(c)}.woff2") format("woff2");
  font-style: {'oblique' if c['style']=='Oblique' else 'normal'};
  font-weight: 400;
}}
```

## Rebuild

From the repository root:

```sh
python -m pip install -r requirements-fourth-cohort.txt
python tools/fourth_cohort/build.py
python tools/fourth_cohort/docs.py
python tools/fourth_cohort/specimen.py
python tools/fourth_cohort/verify.py --require-ots
python tools/fourth_cohort/docs.py --check
python tools/fourth_cohort/specimen.py --check
python tools/fourth_cohort/browser_smoke.py
```

OTS and Chromium installation, isolated builds, report refresh, source provenance
and release limits are in the [cohort workflow](../../docs/FOURTH-COHORT-WORKFLOW.md).
Commit intentional source and regenerated outputs together. The licence covers
this new font software, not unrelated older repository material.
'''
        out[rel+'/OFL.txt']=licence
        rows.append(f"| [{name}](../{rel}/) | {c['lineage']} | {c['style']} | {c['tagline']} |")
    table='| Family | New lineage | Style | Construction / intention |\n|---|---|---|---|\n'+'\n'.join(rows)
    out['docs/FOURTH-COHORT-WORKFLOW.md']=WORKFLOW.replace('__TABLE__',table)
    out['tools/fourth_cohort/OFL.txt']=licence
    return out


def update_indexes():
    """One-time additive publication operation, intentionally not part of rebuild."""
    p=ROOT/'README.md';old=p.read_text(encoding='utf-8')
    if '## Fourth Cohort / 04' in old: raise ValueError('Fourth Cohort already indexed')
    first,rest=old.split('\n',1)
    p.write_text(first+'\n\n'+index_block()+rest.lstrip('\n'),encoding='utf-8')
    for category in ('cmd-font-container','hot-font-box','cachemonic'):
        p=ROOT/category/'README.md';old=p.read_text(encoding='utf-8')
        if '## Fourth Cohort / 04' in old: raise ValueError('Category already indexed')
        rows=['\n## Fourth Cohort / 04\n','| Family | Intent |','|---|---|']
        for rel in FAMILIES:
            if rel.startswith(category+'/'):
                c=config(rel);rows.append(f"| [{c['family']}]({rel.split('/')[1]}/) | {c['tagline']} |")
        p.write_text(old+('' if old.endswith('\n') else '\n')+'\n'.join(rows)+'\n',encoding='utf-8')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');p.add_argument('--index',action='store_true');args=p.parse_args()
    if args.check and args.index:raise SystemExit('--check and --index are mutually exclusive')
    for rel,text in outputs().items():
        target=ROOT/rel
        if args.check:
            if not target.exists() or target.read_text(encoding='utf-8')!=text:raise SystemExit('STALE DOC: '+rel)
        else:target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8')
    if args.index:update_indexes()
    print('38 generated documentation/licence files '+('verified' if args.check else 'written'))
