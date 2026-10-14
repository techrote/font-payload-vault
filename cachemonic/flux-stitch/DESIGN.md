# Flux Stitch — design and construction

## Artistic brief and lineage

Flux Stitch converts the newly drawn Camber curves into an interrupted,
sewn-line appearance. The curve identity is deliberately shared with Camber
Script, but the distribution of ink follows distance along each path, not
horizontal rows or random erased patches. This makes its gaps bend with loops
and tails instead of imitating a scan timing fault.

## Creation technique

Each separate polyline is divided into a whole number of nominal 150-unit
periods. Within each fitted period, 72/150 of the length receives a 44-unit
round stroke. End caps expand the dashes, so the unpainted interval must exceed
the nib width. An early visual check found a shorter interval closed by those
caps; the corrected straight-line regression requires four separated pieces
and more than 25 units between neighbours. A 0.16 shear creates the real
Oblique style. Punctuation is deliberately solid and supporting symbols stay
neutral; the effect is not claimed for every encoded mark.

## Ergonomic or utilitarian intention

The purpose is light, interrupted decorative titles and fictional textile or
signal-path labels. The gaps must remain visible at the composition size or
the artistic distinction from Camber disappears. That is why the new regression
checks disconnected components rather than just different file hashes. This
is not embroidery, toolpath or stitch-machine output. No ergonomic advantage
or suitability for live diagnostics is claimed; it should not carry important
state or transcription content without a plain-text alternative.

## Exact first-release settings

| Property | Value |
|---|---|
| Style | Oblique |
| Pitch | Proportional; tabular digits |
| Figure / default cell | 760 units |
| H / x ink height | 732 / 548 units |
| Trial range | 44–120 px |
| New shared lineage | `camber`; sibling Camber Script |

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
