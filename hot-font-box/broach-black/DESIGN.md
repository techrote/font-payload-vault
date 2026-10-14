# Broach Black — design and construction

## Artistic brief and lineage

Broach Black is the dense display counterpart of the new Quoin skeleton. Its
image is a row of cutting teeth: dark vertical mass punctuated by wedge feet.
The inherited skeleton is disclosed, not passed off as a separately authored
alphabet. It differs from the older Torque Plate and Flypress designs through
Roman curve construction, anisotropic stroke mass and individually selected
wedge-serif sites rather than notched mechanical stock.

## Creation technique

A 152-by-86-unit nib replaces Quoin Serif's lighter 90-by-42 nib. The selected
wedge terminals are 184 units wide and 68 high. Original curves and overlays
are resolved as positive area before export; the counters are the remaining
negative regions, not a hollow-font effect. Letter widths follow the ink span;
figures have 760-unit advances. “Black” is part of the family name describing
the artwork. The sole named style is Regular, with weight metadata 400; no
weight family or Bold style-link is claimed.

## Ergonomic or utilitarian intention

The utilitarian intention is visual hierarchy in short titles and prominent
numeric labels. Broad stems should remain visibly heavier than accompanying
text, but dense counters are a reason not to choose it for small interface
text. Review the separate full alphabet and reduced samples, particularly a/e,
B/8 and sequences involving serifs. No distance-legibility, accessibility,
printing or cutting test is implied by the successful font-software checks.

## Exact first-release settings

| Property | Value |
|---|---|
| Style | Regular |
| Pitch | Proportional; tabular digits |
| Figure / default cell | 760 units |
| H / x ink height | 751 / 537 units |
| Trial range | 42–112 px |
| New shared lineage | `quoin`; sibling Quoin Serif |

## Shared repertoire, geometry and limits

This face has **254 mapped codepoints** and 255 glyph records including `.notdef`:
printable ASCII, Latin-1, defined Windows-1252 additions and selected mathematical,
arrow, light box and block symbols. The full character map is the exact inventory.
It does not include generalized combining-mark positioning, arbitrary non-Latin
scripts, Nerd Fonts or Powerline additions. Prefer supported precomposed letters;
unsupported decomposed sequences can invoke fallback.

The letter/digit skeleton is new artwork. ASCII punctuation is new shared
Fifth Cohort construction, not a separate redraw per family. The unchanged
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
older vault content. Full production details: [Fifth Cohort workflow](../../docs/FIFTH-COHORT-WORKFLOW.md).
