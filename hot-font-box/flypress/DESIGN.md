# Flypress — design and construction

## Repository connection and artistic aim

Flypress belongs in the loud display compartment. The workshop reference is
compressive force: a tall, compact mass that gives a short heading authority.
Unlike Diecast Relay, it has no relief-band motif and does not use small capitals
for lowercase input. Its heavy narrow silhouettes, actual lowercase and compact
word shapes are intended to add a genuinely different display option.

## Positive stock and independently subtracted counters

`source/design.py` defines the alphabet from rectangles, chamfered rings,
explicit polygon perimeters and a limited number of thick stroke paths.
The nominal cap height is 740 units, the lowercase body 520. Principal stems
are 116 units; the ring helper uses 104-unit horizontal and 96-unit vertical
insets, so counters are actual separately controlled negative regions.

`A`, `M`, `N`, `V`, `W`, `S` and `Z` have explicit solid perimeters. `D` has a
flat left spine and a separately constructed angled counter, rather than being
an `O` with another name. The `A` review identified an initially missing upper
counter: it is now explicitly cut as a triangle and protected by a regression.
`m/w` get wider advances; `I` gets a narrow one. Ten digits share 500 units.

Lowercase is separately drawn. `a` combines a low bowl and an upper entry,
`e` has a crossbar and opening, `g` has a lower return and `p/q` retain descenders.
The wide-letter constructions and diagonal stroke widths are selected to retain
usable internal gaps rather than applying a uniform blackening operation to a
thin font. There are no scratches, scanline cuts or stochastic effects.

## Intended use and layout policy

The initial setting is a title, short label, workshop poster, cover or deliberately
condensed numeric callout at 32–96 px. The family has proportional letter spacing,
tabular digits and no kerning table in version 1.000. `usWidthClass` records the
condensed character; the sole named style is Regular. “Heavy” describes this
style's actual drawing, not an additional Bold cut or a developed weight axis.

Narrow widths save headline space, but heavy strokes and compact counters are
poor reasons to choose a body or transcription font. The shared punctuation is
less aggressively condensed than the alphabet to preserve useful operators.
Some supporting Latin and currency recipes are shared production geometry; this
is a complete declared repertoire, not a claim of independently tuned forms for
every linguistic context.

## Limits and next useful review

The typeface has not been distance-legibility tested and is not qualified for
emergency signage, regulated labels or fabrication. It is also not a physical
stencil: a counters-and-stock drawing does not guarantee connected islands,
kerf allowance or a minimum manufactured stroke. Actual installation and
DirectWrite / GDI behavior remain untested.

The first follow-on should be optical spacing in real headlines and the survival
of counters at a specified reproduction size. Changes to the upper `A` hole,
small `a/e`, `B/8`, and `0/O` should be checked in the complete map as well as the
headline that motivated them. Keep the source changes and rebuilt outputs together.

## Shared delivery contract

This is version 1.000, an unhinted outline face, with 254 mapped codepoints:
printable ASCII, Latin-1, defined cp1252 additions and the selected math, arrow,
light box and block symbols listed in the complete map. It does not provide
combining-mark shaping, general non-Latin coverage, a weight axis or a second
style. Precomposed letters are supported; arbitrary decomposed sequences may
use fallback. Native Windows installation, GDI/DirectWrite/ClearType rendering,
physical monitor trials and measured ergonomic benefits remain unclaimed.

The original alphabet is in `source/design.py`; the new shared ASCII punctuation
and drawing conveniences are in `../../tools/workshop_six/common.py`. The existing
`tools/original_trio/geometry.py` and `repertoire.py` are reused as production
helpers without changing their files or importing an old family master. The
production workflow describes this reuse and its limitations. The fonts, source
and these design documents are covered by the accompanying SIL OFL 1.1, with no
Reserved Font Names; this does not relicense older repository material.
