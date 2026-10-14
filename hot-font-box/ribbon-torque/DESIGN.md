# Ribbon Torque — design and construction

## Repository connection and artistic aim

Ribbon Torque supplies the display compartment with an intentionally lighter,
flowing direction. The image is two rails under a small forward load: a ribbon
of metal carrying a curve, rather than a solid stamped letter. This breaks the
vault's predominance of filled angular forms without copying or outlining one
of its existing alphabets.

## New skeleton, united body, hollow rails

`PATHS` and `DIGITS` contain this family's own large-radius curve constructions.
Capitals and genuine lowercase are drawn separately. The positive letter body
uses a 142-unit rounded stroke for letters and 132 for digits. Those positive
parts are united **before** a 36-unit inward offset is removed. The result is
the border of a resolved silhouette, not two accidentally overlapping copies of
a centre line. Internal junctions therefore have a defined Boolean construction.

The hollow body is sheared by x += 0.18*y, approximately 10.2 degrees, then fitted
into its advance with at least 53-unit side margins. Wide letters keep wider
advances; digits share 760 units. The actual installed style is **Oblique**:
OpenType selection flags, `head.macStyle`, `post.italicAngle` and the horizontal
header's caret slope are consistent with that slant. The font is not labeled
upright and left to a browser's synthetic italic operation.

Rounded caps target 731 units with small overshoots; the lowercase body targets
556. The `g` tail was shortened after outline-bound testing found it below the
-250 descent. Dots and punctuation are separately retained; short marks can be
too small to develop a full hollow interior, which is accepted rather than
making essential punctuation disappear.

## Utility is hierarchy, not long-form reading

The intended job is a short title, logo experiment or secondary decorative line
at approximately 48–120 px. Hollow interiors lighten the texture and the slant
provides directional emphasis. Neither property establishes faster reading.
At small sizes the rails and the gap between them can collapse into grey or
inconsistent single strokes. The smallest validation renders are robustness
checks, not recommendations to use this font at 16 px.

Spacing is deliberately open; there is no kerning or ligature feature in this
first edition. It is not a connecting handwriting script. Character joins are
not intended to touch across advance boundaries. This keeps individual letters
inspectable and makes the twin-rail construction useful for short names and
headings, at the cost of economy and the rhythm of a professionally kerned family.

## Supporting characters and boundaries

ASCII punctuation is processed through the ribbon treatment. The extended
repertoire then reuses those bodies and the vault's neutral accent / symbol
recipes. Those added recipes are not all slanted and hollowed a second time.
That mixed treatment is visible in the full character map and is an explicit
first-version limitation, not an assertion of a uniformly inline global font.

The delivered curves are sampled polygon outlines. No native curve editor,
autohinter or existing source font contributes artwork. There is no tested
laser-cut, neon-tube, engraving or accessibility specification despite the
material metaphor. Future work should assess optical spacing, auxiliary-symbol
consistency and rail widths at actual output sizes before adding another weight.

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
