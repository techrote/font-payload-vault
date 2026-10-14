# Camber Script — design and construction

## Artistic brief and lineage

Camber Script adds looped cursive movement to the workshop collection. It is
built from a new set of separately drawn capital, lowercase and figure curves.
The long ascender loops in b/h/l and the returning g/y tails are structural
features of those paths, not synthetic italics applied to Gimbal Sans or an
existing font. Adjacent letters remain unconnected: this is not a handwriting
shaping system with contextual joins.

## Creation technique

The new cubic skeletons are sampled at 24 intervals and expanded by a
90-by-58-unit nib. A shear of x += 0.16*y is then applied before fitting into
proportional advances. Figures share 760 units. The installed style is Oblique;
negative italic angle, oblique/italic selection bits, macStyle and caret slope
are consistent with the nominal shear. Horizontal fitting of an unusually
wide glyph can slightly change its effective angle. The Flux Stitch sibling
uses these new curves with genuine arclength gaps instead of a solid nib path.

## Ergonomic or utilitarian intention

The intended use is a short decorative title or a light contrasting line in
a composition dominated by angular lettering. Open spacing makes individual
loops inspectable but does not reproduce the rhythm of connected handwriting.
It has no contextual alternates or pair kerning. Long ascenders and tails
consume line height; reducing them for dense text is not a tested use. Native
Windows, cursive reading performance and physical tube/engraving suitability
remain separate questions, not accepted features of this release.

## Exact first-release settings

| Property | Value |
|---|---|
| Style | Oblique |
| Pitch | Proportional; tabular digits |
| Figure / default cell | 760 units |
| H / x ink height | 739 / 555 units |
| Trial range | 36–104 px |
| New shared lineage | `camber`; sibling Flux Stitch |

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
