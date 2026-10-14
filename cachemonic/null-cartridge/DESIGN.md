# Null Cartridge — design and construction

## Repository connection and artistic aim

Null Cartridge reverses the usual relationship between letter and background:
the missing material carries the message. Each character is an aperture in a
notched cartridge-shaped field. This is a Cachemonic display experiment for
short labels, decorative identifiers and fictional read-only media, not another
ordinary terminal face with a distress filter.

## A new cutter alphabet, then a field

`PATHS` and `DIGITS` describe an original positive cutter alphabet. Capitals,
true lowercase and numbers are independently specified; all use an 88-unit
bevel-joined stroke. The mechanical grammar is deliberately angular, with
flat walls and clipped shoulders. It is not a reused bitmap or a transformed
Detent Slab master. `0` has a diagonal interior cut, `I` has bars, `1` a flag,
`l` a hooked exit and the pipe a plain vertical cut.

Every encoded character advances 760 units. The standard carrier runs from
x=27 to 733 and y=-242 to 992, with 38-unit corner chamfers and small opposing
edge notches near the midline. The cutter is horizontally fitted with 86-unit
margins. Unusually tall cutters are fitted within y=-202..930 before subtraction,
so accent forms retain a closed field around them instead of cutting through its
outer wall. The field itself stays the same size for lowercase and capitals.

The OpenType cap and x-height values are both 992 because the delivered ink is
the full-height carrier in both cases. The *negative alphabet* inside it has a
nominal upper extent around 744 for caps and 534 for lowercase. This distinction
matters when an application aligns fonts by ink-height metadata rather than by
the baseline.

## Why processing order is important

`draw()` returns positive cutters. The shared repertoire assembler first composes
precomposed accents and removes the original dot from accented lowercase `i`.
Only then does `finalize()` subtract the result from the carrier. Inverting first
would cause the accent code to treat the entire tile as the letter; its dot-removal
operation could clip a large part of the field. The finalizer order is therefore
part of the design contract, and accented-i tiles have explicit bounds regressions.

Spaces and nonbreaking spaces are genuinely blank. Light box drawing, blocks,
arrows and selected functional shapes remain ordinary positive geometry rather
than receiving cartridges. Ordinary punctuation and most other auxiliary
characters receive the reversed field. There are no contextual substitutions:
repeated characters have identical carriers and apertures.

## Intended use, limitations and next review

The suggested first trial is 40–100 px. A cartridge word is intentionally a row
of discrete objects rather than smooth prose. It can provide a strong hierarchy
for a short fictional machine label or a decorative identifier. It is not an
efficient reading font: fields dominate the texture, spaces create conspicuous
gaps, and the meaning of a “black” glyph reverses when the text color changes.

There is no human-factors, safety-signage, stencil or fabrication acceptance.
Neither the black islands nor the apertures have been checked for physical
connectivity, tool diameter or material thickness. Small counters can disappear
at low resolution even though the payload remains structurally valid. Review
tile spacing, accented cutters and contrast in the real composition before use.
The next useful extension would be a separately specified carrier density or
padding variant, not a claim that a normal terminal should render all its text
as these reverse fields.

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
