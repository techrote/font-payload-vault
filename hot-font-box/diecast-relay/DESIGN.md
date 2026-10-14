# Diecast Relay — design and construction

## Brief and artistic goal

`hot-font-box` is the repository's home for loud titles and things large enough
to read across a workshop. The name-idea archive connects that attitude to rat-rod
hardware rather than polished corporate typography. Diecast Relay answers it
with mass, visible tooling and emphatic spacing: letters that resemble marked
castings and cut plate, but do not pretend to be distressed historical lettering.

The aim is not a generic “futuristic font” filter. The main forms should remain
identifiable when the relief-slot effect is removed. A face built solely by
adding scratches to an existing alphabet would not meet that goal. The cap
alphabet and numerals here were authored as their own positive/negative polygon
constructions, independently of the other two new families.

## Solid stock, counters and relief cuts

[`source/design.py`](source/design.py) uses polygons, rectangles and chamfered
rectangles. The upper-case body is nominally 700 units high in a 1000-unit em.
Stem masses are generally around 168 units; bowls use inset counter constructions
rather than expanding the same thin skeleton used by Latchline.

Examples show the design grammar:

- `A` joins two tapered legs with a separate bridge. Its apex is deliberately
  broad, not the convergence of hairline diagonals.
- `O` is a chamfered outer shell with a smaller chamfered counter. `D` instead
  keeps a flat left wall and angled right shoulders; a visual review prompted
  that distinction because an all-around chamfer made it too similar to `O`.
- `B` combines a vertical mass with two differently sized bowls; `R` adds a
  descending wedge to the upper bowl. `M` and `W` have drawn interior notches
  and separately chosen wider advances.
- `S`, `2`, `5` and `Z` have explicitly listed perimeter vertices. They are not
  cut-and-paste versions of the bowl glyphs.

After the letter is assembled, two 27-unit horizontal relief bands are subtracted
from `A B D O P Q R 0 4 6 8 9`, at 224–251 and 486–513 units. The cuts break the
otherwise solid cast-metal rhythm. They are applied only to the selected forms,
not indiscriminately through every character. The visibly interrupted bowls
alternate with uninterrupted solid letters such as `E`, `H` and `T`.

Geometric unions remove overlapping ink before serialization. Coordinates are
snapped to integer units; contours are oriented and ordered deterministically.
Most cap outlines are therefore direct polygon geometry. Supporting punctuation,
accents and symbols also use a small number of sampled curved primitives where
an all-angular interpretation would obscure the character.

## Case and spacing are part of the artwork

ASCII lowercase is deliberately **small capitals**. Each small-cap glyph is
created from its corresponding cap construction with 0.78 vertical scale and
0.84 horizontal scale around the design bearing, then assigned its own smaller
advance. It is not a claim to optically compensated, independently redrawn
small-cap masters. The lighter apparent weight is an accepted first-version
trade-off. Accented lowercase follows this same small-cap policy.

This transformation is restricted to this family's caps. It does not mean the
three families share a common master. The uppercase cap constructions are
independent of Latchline and Cache Rattle.

Widths are intentional: `I` is narrow, `M` and `W` are wide, and `J`, `L`, `F`
and `T` have their own values. All ten digits retain a 660-unit advance for
short prices, serial numbers and measurements. The face is not monospaced, even
though the numeral set is tabular. A small GPOS `kern` feature contains exactly
ten pairs: `AV AW AY AT VA WA YA TA To Te`. There is no `GSUB`, no ligature
feature and no contextual replacement. Small-cap input does not depend on a
layout engine enabling an optional feature.

The sole installed style is **Regular**, with weight metadata 400. “Heavy”
describes the drawing, not a second Bold style. This avoids pretending that a
weight family has been developed and keeps CSS use straightforward.

## Utilitarian intentions and explicit exclusions

The intended utility is short-message hierarchy: a display word should look
materially different from a supporting terminal log. Strong silhouettes, broad
strokes and tabular numerals are intended to make workshop-themed titles and
numeric labels organized and forceful. Short labels at 32–96 px are the initial
trial context. Distance legibility has not been measured.

Fine bands disappear sooner than the main strokes as text is reduced, so a font
size alone does not guarantee that the motif survives. Monitor scale, export
resolution, ink spread, contrast and rendering mode change the result. The
small capitals are poor substitutes for genuine text lowercase in long prose.
This is intentionally not the family's job.

Despite its construction vocabulary, this is an **optical stencil motif**.
No manufacturing qualification has checked cut bridges, island connectivity,
kerf, material strength or minimum physical stroke width. Converting the text
straight to a laser/CNC toolpath is not accepted by this font's tests. It is
also not intended for emergency instructions, regulated signage or other
safety-critical text without a separate suitability assessment.

## Review and continuation

Rendered cap/small-cap, number, accent and punctuation sheets were inspected.
Automated tests verify proportional-versus-fixed metadata, tabular digit
advances, smaller lowercase heights, the D/O distinction and absence of polygon
collisions in the declared kerning pairs. These are geometry and layout checks,
not a substitute for human headline-composition review.

Future work should concentrate on optical small-cap weight, pair spacing outside
the small initial kerning set, and relief widths at specific reproduction
sizes. A true physical-stencil derivative needs its own design contract. Keep
the original masters and regenerate outputs together; do not repair the compiled
font without recording the construction change.
