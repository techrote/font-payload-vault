# Punchloom — design and construction

## Artistic brief and lineage

Punchloom reinterprets the new Pinfeed grid as a woven field. The underlying
letters are intentionally shared with Pinfeed Grid: this is a pair of related
faces with different material treatments, not two independent handwritten
alphabets. The parent grid itself was newly entered for this cohort and has
no copied earlier font cells.

## Creation technique

Each occupied 60-unit cell becomes a skewed quadrilateral with a rectangular
internal slit. The outer primitive has four vertices:
(3,7), (54,1), (59,53), (7,59), relative to the cell origin. Row-plus-column
parity selects a vertical or horizontal 12-unit-wide slit. The alternating
cut direction suggests over/under threads while leaving each cell at its
original position. Neighbouring modules do not grow into an extruded shadow.
Advances remain 640 units and the i-dot boundary fix is shared with Pinfeed.

## Ergonomic or utilitarian intention

The useful constraint is repeatability in fixed-cell decorative layouts.
The woven texture is best assessed at large sizes; small samples are only
robustness checks and may look like uneven grey pixels. It is not a raster-font
strike, knitting instruction, weave simulation or manufacturing pattern.
Auxiliary symbols and accents use the neutral repertoire engine rather than
pretending all Unicode shapes were separately woven. Do not use this face as
the only rendering of alarms, credentials or important numeric identifiers.

## Exact first-release settings

| Property | Value |
|---|---|
| Style | Regular |
| Pitch | Fixed |
| Figure / default cell | 640 units |
| H / x ink height | 659 / 419 units |
| Trial range | 54–140 px |
| New shared lineage | `pinfeed`; sibling Pinfeed Grid |

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
