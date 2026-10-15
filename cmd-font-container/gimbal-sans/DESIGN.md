# Gimbal Sans — design and construction

## Artistic brief and lineage

Gimbal Sans offers a proportional, comparatively quiet answer to the vault's
instrument theme. The gimbal metaphor is articulation rather than rigidity:
open curves, noncircular shoulders, varied widths and a measured stroke contrast.
Its new GIMBAL path set is not the Bushing or Collet alphabet. Capitals and real
lowercase were authored separately, with wider m/w and narrower i/l/r.

## Creation technique

A 76-by-68-unit elliptical nib expands the sampled original cubic paths. The
unequal axes give verticals slightly more mass than horizontals. Bowls are
resolved from complete paths, and overlaps are united before integer contour
export. Letter advance follows the actual ink span plus bearings; figures share
650 units. The related Orbit Hatch uses the same newly drawn paths with a much
heavier body and explicit perimeter-plus-hatching construction.

## Ergonomic or utilitarian intention

The use hypothesis is short prose around instruments, menu labels and numeric
readouts. It is not fixed pitch and should not replace a terminal's cell font.
Slashed zero, flagged one and a hooked l aid shape differentiation in short
strings; narrow counter and confusable checks exercise those exact drawings.
There is no kerning program, so AV/To and mixed punctuation still need optical
spacing review. No reading-speed or fatigue benefit has been measured.

## Exact first-release settings

| Property | Value |
|---|---|
| Style | Regular |
| Pitch | Proportional; tabular digits |
| Figure / default cell | 650 units |
| H / x ink height | 747 / 553 units |
| Trial range | 18–30 px |
| New shared lineage | `gimbal`; sibling Orbit Hatch |

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
