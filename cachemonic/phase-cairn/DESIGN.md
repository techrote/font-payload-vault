# Phase Cairn — design and construction

## Artistic brief and lineage

Phase Cairn takes the newly drawn Octant skeleton apart into small oriented
stones. It is the experimental sibling of Octant Cut, with an explicitly shared
new alphabet. Its reference is a path recovered from separated markers, not a
corrupted file or a shuffled character encoding. Character identity and advance
remain fixed even though the apparent stroke becomes fragmented.

## Creation technique

Each separate source polyline is split into a whole number of intervals with
a nominal 104-unit period. A four-vertex stone is placed at each interval's
midpoint and aligned with the local path tangent. Its longitudinal half-length
is at most 46 units, further limited to 40% of the actual interval; its transverse
half-width is 43 units. The resulting negative gaps are explicit geometry.
All encoded characters retain a 720-unit advance. Widened source dot segments
keep i/j markers substantial rather than degenerate slivers.

## Ergonomic or utilitarian intention

The intended utility is a stable grid for decorative broken inscriptions and
fictional archaeological/electronic graphics. The sparse stones are likely to
lose or change texture when reduced, so the robustness renders do not endorse
them for practical text. There is no seed, temporal animation, substitution or
image-based effect. Accents, arrows and functional box/blocks remain neutral
shared geometry. Important status, alarms and identifiers need a separate
plain rendering; no human-factor or fabrication suitability is inferred.

## Exact first-release settings

| Property | Value |
|---|---|
| Style | Regular |
| Pitch | Fixed |
| Figure / default cell | 720 units |
| H / x ink height | 686 / 496 units |
| Trial range | 48–128 px |
| New shared lineage | `octant`; sibling Octant Cut |

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
