# Anode Bloom — design and construction

## Repository connection and artistic aim

Anode Bloom is an experiment in apparent electronic persistence, not damaged
bytes. It belongs in Cachemonic because its texture deliberately interferes with
normal continuous letter strokes, but it does not reuse Cache Rattle's grid or
row-tearing transformation. Its alphabet is a new six-column matrix, and every
node stays exactly where it was drawn.

## The complete ASCII grid is source artwork

`GRID` in `source/design.py` contains all 95 printable ASCII entries. Rows have
exactly six columns: `#` is an emitter and `.` is empty. `/` separates rows.
Capitals normally use nine rows. Lowercase has meaningful leading blank rows,
its own body patterns, and additional rows where a descender is needed. The
parser rejects a wrong row width, unknown cell symbol or excessive row count.
No bitmap capture, installed font, downloaded font or pre-existing pixel master
is used as a design input.

Columns are 90 units apart, starting at x=135; rows are 80 units apart, starting
at y=700. The 720-unit advance is constant. A filled cell becomes a 25-unit-radius
solid emitter **plus a separate annular halo** with outer radius 38 and inner
radius 31. The six-unit radial gap between the emitter and halo is real negative
space, not alpha transparency. Both parts are ordinary monochrome outlines.

That repeated core-and-halo structure is the “bloom.” There is no colored glow,
bitmap texture, runtime effect or time seed. The exported geometry is identical
on every build. The upper ink height is 738 and the lowercase body target 498.
The zero includes diagonal internal nodes; `I`, `l`, `1` and pipe have separately
drawn patterns, although these distinctions are not enough to make a decorative
dot font a recommended operational interface.

## Artistic and utilitarian trade-offs

The intended setting is fictional electronics, cover art, short titles and
staged readouts, initially at 48–120 px. A fixed cell makes these compositions
predictable. The halo gives larger lettering a distinctive perforated edge
without requiring a shader, image filter or multicolor-font implementation.

Small rendering sizes can make the thin halo vanish, merge with the emitter or
become a grey fringe. That is an output-size limitation, not actual random
corruption. The six-column grid is not a set of per-size raster strikes; there
is no pixel-exact size claim. It should not be the only rendering of alarms,
credentials, important serial numbers or accessibility text.

## Extended repertoire and review boundary

The full font maps 254 codepoints. Extended accents, currencies, fractions and
functional symbols are assembled by the existing neutral repertoire engine from
these bodies and explicit geometric recipes. They are not all redrawn as emitters.
Light boxes, arrows and blocks remain clean, so direction and cell structure are
not accidentally fragmented. This mixed texture is intentional and documented.

The regression checks protect the complete grid, node separation, fixed pitch,
nonempty glyphs, bounds and reproducible exports. They do not validate screen
comfort or reading performance. Review the complete map in both polarities at
the actual output size; an alternate low-density or emitter-only cut should be
versioned as a separate design rather than silently changing this halo geometry.

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
