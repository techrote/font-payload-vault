# Latchline Mono — design and construction

## Brief and repository connection

The `cmd-font-container` category asks for things that belong in a console,
taskbar, start menu or DOS box. Knurled Swarf supplies a pixel-accurate answer.
Latchline instead asks what a latched, stable machine state would look like as a
scalable outline alphabet. It borrows the repository's workshop vocabulary and
plain-text rebuild philosophy, **not Knurled Swarf's glyphs, grids or metrics**.

The name combines a hardware latch with the line occupied by a terminal record.
Its visual objective is quiet precision: workbench instrumentation rather than
neon cyberpunk decoration. Squared round forms and explicit stroke endings imply
machined components without putting distress into operational text.

## Independently drawn centre-line master

[`source/design.py`](source/design.py) contains a complete, independently authored
printable-ASCII design. `PATHS` is the master, expressed as `M`, `L`, `C` and `Z`
commands in an upward-positive 1000-unit coordinate system. It is not an SVG
extracted from another font. No installed or downloaded font supplies outlines.

Straight stems, crossbars and diagonals are specified separately. Rounded bowls
use explicit cubic control points: straight-ish sides meet round shoulders rather
than forming geometric circles. The shared geometry engine samples each cubic
at 20 intervals, expands the centre line with a 72-unit stroke, unites overlaps,
and rounds coordinates to whole font units. Stroke buffers use 12 segments per
quarter circle. The delivered TrueType outlines therefore consist of short
straight segments; they are **not native quadratic Bézier contours**. This choice
makes the procedural pipeline inspectable, at the cost of more outline points
and eventual visible faceting at unusually large magnification.

Corners have rounded joins but flat caps. Caps usually occupy 0–700 units;
rounded caps overshoot slightly. Lowercase body height targets 520 units, with
ascenders around 724 and descenders generally around −205. Individual letters
are optical constructions, not automatically scaled capitals. `a` has a bowl
under an upper entry stroke; `g` has a separate descending hook; `r` exposes its
shoulder. `m` and `w` are drawn to occupy the fixed cell rather than compressed
from wider proportional forms.

The independent master includes punctuation and digits, not only letters.
Accents and auxiliary symbols are constructed from this family's own components
by `tools/original_trio/repertoire.py`. In accented `ì í î ï`, the ordinary dot is
removed before the accent is positioned; it is not left underneath the accent.

## Character identity as an ergonomic intention

| Pair or group | Actual drawing decision | Intended utility |
|---|---|---|
| `I l 1 |` | `I` has top/bottom bars; `l` has a hooked lower exit; `1` has a diagonal flag and foot; the pipe is a plain taller stem. | Reduce ambiguity in identifiers and transcribed values. |
| `O 0 Ø` | `0` is narrower and slashed; `O` is an unslashed bowl; `Ø` uses the alphabetic bowl and a different slash. | Separate letters, numbers and the Scandinavian letter. |
| `B 8` | `B` has a left spine; `8` is two independent rounded bowls. | Keep numeric diagnostics distinct from hexadecimal letters. |
| `g q` | `g` has a returning descender; `q` has a straight right descender. | Avoid relying on context in short identifiers. |
| Operators | Dedicated punctuation, no `GSUB` ligatures and no kerning. | Preserve the literal number and positions of typed characters. |

The font has the same advance for every encoded glyph, including spaces,
precomposed accented letters and symbols, and advertises fixed pitch in its
OpenType `post` table. This is a measurable layout property. It is **not evidence
that people read the face faster or make fewer mistakes**. The initial 16–24 px
range is a design target, not an accessibility certification.

## Cell geometry and limits

The nominal advance is 640 units. Ascender/descent metadata is 1000/−250 with zero
additional line gap. This leaves room for capitals with accents and gives the
included light box-drawing set a 1250-unit vertical cell. Horizontal box lines
reach both advance boundaries. Vertical connectors reach both line boundaries;
half blocks reconstruct the full block exactly. The draw coordinates join, but
an application's line-height override, raster rounding or cell policy can still
make a visible seam. Double lines, all Unicode box variants and braille are not
included.

This first release has no instructions for TrueType grid fitting and no embedded
bitmap strikes. Small-size rendering depends on the rasterizer. No Windows font
installation, ClearType/DirectWrite/GDI comparison, physical monitor assessment or
extended daily-use trial has been completed as part of this design. A terminal
that substitutes unsupported symbols can also mix advances or stroke weights.

## Review and useful next edits

The construction was inspected in rendered alphabet, pangram, numeral,
confusable and accent sheets. Automated checks verify the exact exported
coordinates, common confusable glyphs at 16/18/24 px, and enclosed raster
counters for selected characters at 18/24/32 px. Those checks are deliberately
narrow: different pixels and surviving counters do not establish human usability.
See the repository verification record for the actual build, not an assumed pass.

A useful daily-use review would log troublesome characters at the actual terminal
size, scaling and renderer. Change those masters first, then rerun the entire
build. A dedicated hinted or pixel-size variant would be a separate project;
scaling this outline down and claiming Knurled Swarf-style pixel accuracy would
not be justified.
