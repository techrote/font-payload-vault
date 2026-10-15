# Octant Cut — design and construction

## Artistic brief and lineage

Octant Cut starts from a new faceted alphabet. The main bowls are elongated
many-sided paths, not rounded sans shapes with a bevel applied afterwards.
Capital A has side walls and a roof; O is a tall faceted loop; lowercase a/e/g
retain their own body structures. This new OCTANT skeleton is independent of
RAIL, even though both use straight segments. Its geometric inscription-like
rhythm is the artistic objective, not a reconstruction of a historical script.

## Creation technique

A 113-by-82-unit anisotropic nib with flat caps and bevel joins expands the
new paths. Proportional advances fit the faceted silhouettes, while figures
share 700 units. Explicitly widened 52-unit i/j dot strokes prevent a flat-cap
one-unit source segment from disappearing into a hairline. Phase Cairn shares
this new skeleton but samples it as separated tangent-aligned stones. That
relationship is intentional and documented.

## Ergonomic or utilitarian intention

The use hypothesis is narrow monumental headings and distinctive short
workshop labels. Facets are meant to survive as a clear silhouette, with real
lowercase available for mixed-case titles. The pointed bowls and compact
counter rhythm are poor grounds for a small body-text recommendation. It has
not been tested as stone carving, laser lettering, an emergency notice or a
manufactured stencil. Review at the reproduction size before relying on it.

## Exact first-release settings

| Property | Value |
|---|---|
| Style | Regular |
| Pitch | Proportional; tabular digits |
| Figure / default cell | 700 units |
| H / x ink height | 696 / 523 units |
| Trial range | 36–104 px |
| New shared lineage | `octant`; sibling Phase Cairn |

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
