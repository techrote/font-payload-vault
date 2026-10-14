# Collet Sans — design and construction

## Repository connection and artistic aim

Collet Sans occupies the system-UI compartment, but is deliberately **proportional**.
Knurled Swarf already handles individually tuned small pixels and Latchline Mono
handles a fixed instrument cell. This face instead suggests the smooth gripping
surface of a collet: a quiet tool that holds a label without advertising itself.
Broad oval bowls and open `C/c` apertures contrast with the more rectilinear work
elsewhere in the vault. It is not a historical face recreation.

## How the master is made

`source/design.py` explicitly assigns an original geometry and advance to all
52 letters and ten digits. Most bowls use an ellipse with a separately specified
inner ellipse subtracted: the principal side thickness is 80 units and the top /
bottom thickness is 68. The light contrast is therefore constructed, not a
weight filter applied to another typeface. Straight stems are rectangles;
shoulders, tails and difficult letters such as `S`, `g` and `s` use authored cubic
centre lines expanded to strokes. Component unions resolve the overlaps.

The cap target is 720 units and the lowercase body target is 535. `a` has a lower
bowl and a distinct upper entry; `g` has its own returning descender. Neither is
a scaled capital. `m` and `w` receive wider drawings and advances, while `i`, `l`
and `r` receive narrower ones. Ten digits share a 600-unit advance, even though
the rest of the family is proportional. There is no kerning table or contextual
shaping in this first release: spacing is entirely in the advance widths.

Rounded shapes overshoot the nominal baseline / height slightly. The local
review exposed a `g` extending below the declared -250 line descent; its control
points were corrected instead of increasing the clipping allowance. The rounded
geometry is sampled and quantized by the existing shared geometry helper; the
TTF consists of polygonal outlines, not native quadratic Bézier curves.

## Practical intention, not a study result

The design target is relatively calm interface labels, compact prose around
instruments and occasional numeric readouts. A barred `I`, flagged `1`, hooked
`l`, plain pipe and slashed zero give short identifiers more than one shape cue.
The mono digit set supports columns of values without making prose monospaced.
Initial inspection sizes are 18–28 px, not a guarantee about every renderer.

The practical-font tests check distinct raster signatures for selected
confusables at 18/22/28 px and retained counters at 22/28/36 px. Those are narrow
engineering checks: different pixels and open counters do **not** prove reduced
fatigue, improved reading speed, dyslexia suitability or accessibility. Because
ordinary letters have different advances, this is not a terminal-grid replacement.

## Coverage, review and future edits

The Latin alphabet and numerals are new drawings. ASCII punctuation comes from
the new cohort's explicit common recipes, fitted to proportional advances.
Precomposed Western Latin, currency, auxiliary symbols and light box drawing
use the vault's existing repertoire assembler with this family's own bodies.
Some supporting symbols therefore share the vault's neutral construction grammar.
Accented narrow letters may be horizontally fitted to their advances; they are
not individually optically mastered international-language variants.

Review alphabet, accents, numeric pairs and mixed-case prose in the included
specimen before adopting the font in a real UI. The next useful work is spacing
around difficult pairs and actual Windows renderer / display-scale trials, not
claiming that the present geometry tests have already established those results.

## Shared delivery contract

This is version 1.000, an unhinted outline face, with 254 mapped codepoints:
printable ASCII, Latin-1, defined cp1252 additions and the selected math, arrow,
light box and block symbols listed in the complete map. It does not provide
combining-mark shaping, general non-Latin coverage, a weight axis or a second
style. Precomposed letters are supported; arbitrary decomposed sequences may
use fallback. Native Windows installation, GDI/DirectWrite/ClearType rendering,
physical monitor trials and measured ergonomic benefits remain unclaimed.

The original alphabet is in `source/design.py`; the new shared ASCII punctuation
and drawing conveniences are in `../../tools/workshop_six/common.py`. The existing
`tools/original_trio/geometry.py` and `repertoire.py` are reused as production
helpers without changing their files or importing an old family master. The
production workflow describes this reuse and its limitations. The fonts, source
and these design documents are covered by the accompanying SIL OFL 1.1, with no
Reserved Font Names; this does not relicense older repository material.
