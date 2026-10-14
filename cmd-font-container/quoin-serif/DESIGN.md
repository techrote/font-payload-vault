# Quoin Serif — design and construction

## Artistic brief and lineage

Quoin Serif introduces wedge-serif text into a vault dominated by technical
sans and pixel work. A quoin holds a printing forme; the image here is letters
secured by small wedges. The newly authored Roman skeleton is independent of
the new sans, rail, cursive, facet and grid alphabets. It includes separate
lowercase, an exiting l, a slashed zero and non-identical B/8 construction.

## Creation technique

The positive body is drawn with an anisotropic 90-by-42-unit nib. The apparent
stroke contrast therefore comes from geometry, not a contrast filter on an
existing font. Explicit FEET and TOPS tables select serif attachment sites;
162-unit-wide, 56-unit-high six-vertex wedges appear only there. They are not
added at every node of a curve. Quoin's Broach Black sibling uses 152-by-86
stock and larger wedges; both openly share this new skeleton lineage.

## Ergonomic or utilitarian intention

The intention is short explanatory text, captions and workshop editorial
compositions at a larger trial size than the sans. Wedge terminals give a
horizontal anchoring rhythm while thin cross-strokes keep the texture open.
They can also vanish under reduction or gain too much prominence on coarse
screens. The practical counter tests begin at 24 px, not at tiny menu sizes.
This first version has no kerning, hinting, print trial or prolonged reading
study; such assessments precede claims about body-text suitability.

## Exact first-release settings

| Property | Value |
|---|---|
| Style | Regular |
| Pitch | Proportional; tabular digits |
| Figure / default cell | 680 units |
| H / x ink height | 729 / 515 units |
| Trial range | 24–38 px |
| New shared lineage | `quoin`; sibling Broach Black |

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
