# Pinfeed Grid — design and construction

## Artistic brief and lineage

Pinfeed Grid follows continuous paper-feed machinery rather than another
sparse dot display. Its new eight-column alphabet uses eleven nominal capital
rows; lowercase has four leading blank rows and separately drawn bodies, with
additional descender rows where required. The grids are new source artwork,
not extracts of Knurled Swarf, Nibble Nine, Cache Rattle or an installed font.

## Creation technique

Each filled cell becomes a 60-unit square, and adjacent cells are united into
continuous stock. Eleven rows reach 660 units; the seven-row lowercase body
reaches 420. Every encoded character has a 640-unit advance. The i dot is raised
two units above the shared accent-removal boundary so replacing it cannot leave
a zero-area edge or a residual dot. Punchloom shares this newly entered grid,
but replaces solid cells with explicitly notched over/under modules.

## Ergonomic or utilitarian intention

The intended setting is controller-like labels, short terminal experiments
and fixed-cell diagrams. Continuous blocks provide a denser alternative to
separated emitters. The 8-column width permits separate I/l/1 and a diagonally
marked zero; it also makes m/w quite dense. These are scalable outlines with
no bitmap strikes or pixel-hinting acceptance. “Grid” does not promise a clean
pixel at every font size. Rendering below the stated trial range is inspection,
not a guarantee of practical usability.

## Exact first-release settings

| Property | Value |
|---|---|
| Style | Regular |
| Pitch | Fixed |
| Figure / default cell | 640 units |
| H / x ink height | 660 / 420 units |
| Trial range | 24–40 px |
| New shared lineage | `pinfeed`; sibling Punchloom |

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
