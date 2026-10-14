# Detent Slab — design and construction

## Repository connection and artistic aim

Detent Slab is the second practical face: an angular monospaced alphabet with
selected slab terminals. A detent is a positive mechanical stop; the visual idea
here is that every character lands in a definite register. The aim is a lightly
machined typewriter rhythm rather than another smooth monoline or another
low-resolution DOS grid. The face lives alongside, not over, Knurled Swarf and
Latchline Mono.

## Independent skeletons and selective slabs

The `PATHS` and `DIGITS` dictionaries are the original masters. Capitals, true
lowercase and digits have separately authored coordinates. Rounded-looking
bowls are actually explicit straight-sided, chamfer-shouldered loops. A 76-unit
stroke with bevel joins builds their body; an additional pair of tables (`FEET`
and `TOPS`) states exactly which terminals receive rectangular slabs.

Slabs are 156 units wide and 57 high. They are **not** attached to every vertex:
that would fill counters and make diagonals needlessly noisy. The wide capital
`I` has drawn bars, `l` has a descending stem and right-hand exit, and `1` uses an
angled flag and separate foot. The zero has a centre dot rather than Collet's
slash. `g` returns through a lower tail, while `q` has a straight descender.

Each encoded glyph, including all auxiliaries and spaces, advances exactly
720 units. Capitals target 730 units high, lowercase 538, and the line metrics
are 1000/-250 with no extra line gap. Lowercase `m` is explicitly designed for
the cell rather than horizontally compressing a proportional master. Ordinary
punctuation uses the new common recipes with the same fixed advance. There are
no ligatures, alternate-character substitutions or kerning pairs.

## Utilitarian intention and trade-offs

The intended setting is tabular records, instrument labels, source listings and
terminal text at roughly 20–30 px. Slabs give narrow stems a stronger horizontal
presence, while fixed advances keep values and columns aligned. The angular
interiors distinguish this face from the smooth sans and slashed-outline work
in the same release. These are design hypotheses, not measured human-factor gains.

Slabs also consume space. At small raster sizes they can produce a denser texture
than the nominal 76-unit stems suggest. The mono `m/w`, the two-storey `a` and
tightly arranged numerals deserve particular attention on the intended screen.
The tests check selected confusable pairs and enclosed counters at specified
sizes, but do not certify prolonged terminal use or Windows console availability.

## Functional geometry and acceptance boundary

The included light box set and blocks use the shared cell generator. Their
outline edges reach the 720-unit horizontal cell and the declared 1250-unit
line cell; complementary block halves reconstruct a full block. Actual seams
still depend on application line height, fallback and raster rounding. This is
not the entire Unicode box-drawing repertoire, braille, Powerline or Nerd Fonts.

The face is an unhinted scalable outline, not a per-pixel master. There are no
embedded strikes and no claim of Knurled Swarf's pixel-exact behavior. Review the
provided counter / confusable samples at the exact renderer and scaling where
it will be used. A hinted or size-specific edition would need its own acceptance
work rather than being implied by this first release.

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
