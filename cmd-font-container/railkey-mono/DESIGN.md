# Railkey Mono — design and construction

## Artistic brief and lineage

Railkey Mono is the practical end of the new rail lineage. The starting image
is a bank of latched terminals: straight channels, folded shoulders and a fixed
register. It is not a redraw of Tracebar or Latchline; its 62 letter/figure paths
were entered independently in `masters/rail.py`. Capital A has a short flat apex,
C has long vertical sides, and the g descender returns beneath the body rather
than copying q. Narrow letters are drawn to occupy a full terminal cell.

## Creation technique

The original M/L/Z skeletons are expanded with a 78-by-78-unit nib, flat caps
and bevel joins. Horizontal placement is normalized into 680-unit advances;
wide m/w remain within their cells. There are no random cuts, layout ligatures
or kerning. The same new skeleton also supports Flange Banner, whose broader
nib and attached tabs are a different display treatment, not a second hidden
master. Railkey keeps those tabs out of practical text.

## Ergonomic or utilitarian intention

The intended trial is source listings, tabular diagnostics and instrument
labels. Barred I, flagged 1, an exiting l and a taller plain pipe supply distinct
shape cues. Zero has its own narrower loop and a slash, not an O alias. Fixed
advances preserve literal columns; that is a geometry property, not a claim of
fewer transcription errors. Wide tracking and comparatively squared lowercase
are deliberate costs. Test terminal fallback and the actual size before use.

## Exact first-release settings

| Property | Value |
|---|---|
| Style | Regular |
| Pitch | Fixed |
| Figure / default cell | 680 units |
| H / x ink height | 700 / 545 units |
| Trial range | 18–30 px |
| New shared lineage | `rail`; sibling Flange Banner |

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
