# Orbit Hatch — design and construction

## Artistic brief and lineage

Orbit Hatch is an engraving experiment using the freshly drawn Gimbal
skeleton, not an effect applied to an older vault font. Its visual contrast is
between a continuous letter boundary and a striped interior: the outline says
stable object, while the interior reads as a material surface. It deliberately
avoids the previous cohort's scanline tearing and displaced ghost imprints.

## Creation technique

The body is first expanded with a heavy 156-by-138-unit nib. An 18-unit inner
inset defines a continuous perimeter band. That band is united with the body
intersected by 12-unit-wide, 45-degree hatch strokes placed at 58-unit horizontal
intervals. The whole construction remains monochrome ordinary contours: there
is no image fill, shader, opacity or runtime randomness. Letter widths are
proportional and figure advances are 740 units. Supporting accent and currency
recipes remain neutral rather than receiving a second hatch treatment.

## Ergonomic or utilitarian intention

The intention is short large headings or fictional instrument artwork with
a repeatable engraved surface. Hatch lines and the narrow perimeter are highly
scale-dependent; low-resolution output can turn them into grey texture. No
measured reading advantage is claimed, and the family is not an operational
alert or transcription face. Neither the hatch spacing nor the inset specifies
a tool diameter or physical engraving process. Composition at the actual
output scale is required before aesthetic acceptance.

## Exact first-release settings

| Property | Value |
|---|---|
| Style | Regular |
| Pitch | Proportional; tabular digits |
| Figure / default cell | 740 units |
| H / x ink height | 782 / 588 units |
| Trial range | 54–140 px |
| New shared lineage | `gimbal`; sibling Gimbal Sans |

## Shared repertoire, geometry and limits

This face has **254 mapped codepoints** and 255 glyph records including `.notdef`:
printable ASCII, Latin-1, defined Windows-1252 additions and selected mathematical,
arrow, light box and block symbols. The full character map is the exact inventory.
It does not include generalized combining-mark positioning, arbitrary non-Latin
scripts, Nerd Fonts or Powerline additions. Prefer supported precomposed letters;
unsupported decomposed sequences can invoke fallback.

The letter/digit skeleton is new artwork. ASCII punctuation is new shared
Fourth Cohort construction, not a separate redraw per family. The unchanged
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
older vault content. Full production details: [Fourth Cohort workflow](../../docs/FOURTH-COHORT-WORKFLOW.md).
