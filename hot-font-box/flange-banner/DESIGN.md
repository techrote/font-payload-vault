# Flange Banner — design and construction

## Artistic brief and lineage

Flange Banner moves the rail lineage out of operational text and into broad,
forceful headings. Its reference is an extruded section with attachment tabs,
not distressed paint or a historical factory sign. It intentionally shares the
newly drawn rail skeleton with Railkey Mono, while changing mass, spacing and
the treatment of long verticals. It is not an independently drawn second rail
alphabet, and the provenance does not pretend otherwise.

## Creation technique

The body uses a 140-by-110-unit nib with flat caps and bevel joins. Only
vertical source segments longer than 270 units receive tabs. Two attachment
positions, at 8% and 92% of each qualifying segment, add 206-by-44-unit flanges.
Those positive pieces are united with the body before serialization. Letters
have proportional advances and figures share 800 units. No scanline is removed
and no contour is offset into a fake shadow.

## Ergonomic or utilitarian intention

The purpose is headline hierarchy and material character in short workshop
labels. The long-stem tabs create a different cadence from the quieter mono
without making every corner equally noisy. Dense lowercase, strong bearings
and unkerned capitals cost space. Trial it in real headings before reducing it.
Neither the tab dimensions nor the word “flange” constitutes a fabrication,
physical stencil or safety-signage specification.

## Exact first-release settings

| Property | Value |
|---|---|
| Style | Regular |
| Pitch | Proportional; tabular digits |
| Figure / default cell | 800 units |
| H / x ink height | 700 / 549 units |
| Trial range | 40–104 px |
| New shared lineage | `rail`; sibling Railkey Mono |

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
