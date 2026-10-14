# Cache Rattle — design and construction

## A bounded answer to Cachemonic

The `cachemonic` category explicitly welcomes cursed grids and generative
weirdness. Cache Rattle treats that as a design brief, not permission to ship a
randomly damaged font file. Its goal is controlled visual interference: the
alphabet remains mostly recoverable while the horizontal timing appears wrong.
The sound implied by “rattle” belongs to a loose part, repeated bus noise or
workshop vibration, rather than an elaborate occult narrative.

The design is suitable for a fictional corrupt cache readout or a title that
needs to feel unstable. The actual payload must remain structurally valid,
repeatable and straightforward to inspect. Visual corruption and data
corruption are deliberately separate.

## The bitmap master is new artwork

[`source/design.py`](source/design.py) contains the complete printable-ASCII
master as slash-separated text rows. Every row has seven columns. `#` is ink;
`.` is empty. Capital forms usually occupy nine rows; lowercase uses empty top
rows, its own body drawings and, where needed, additional descender rows.
Punctuation and numerals are explicitly drawn too. No source font, raster
capture, pre-existing grid or Knurled Swarf master was imported.

The letter design precedes the glitch. `I` is bar-topped and bar-footed, `1` has a
flag, `l` has an exit foot, and `0` has internal diagonal ink. Lowercase `a`, `e`,
`g`, `m` and `r` have their own row patterns rather than being reduced capitals.
These distinctions provide a recognizable substrate, even though the effect
intentionally makes reading less comfortable than Latchline.

Each column spans 68 font units. Rows are spaced 78 units apart, with the bottom
10 units of each row left empty. The top cap boundary is 700 units. These
horizontal gaps survive in the scalable outline as separate strips; they are
not antialiasing errors. Adjacent filled cells in a row are united into longer
strips before export.

## Deterministic row tearing

For each ASCII character `c`, the generator hashes the UTF-8 string
`cache-rattle-v1:` followed by `c` using SHA-256. Two byte values select the tear
rows: one row in the range 2–4 moves left by 32 units, and one in 5–7 moves right
by 38 units. All other rows retain their original horizontal position. The
constant phase string is part of the design identity.

The rule changes row position, **not character advance**. A letter still occupies
a 660-unit cell, and the checked outline stays within it. It neither deletes an
entire row nor randomly substitutes another character. Punctuation is governed
by the same rule, although a selected tear row may be empty for a particular
punctuation mark. There is no requirement that every glyph visibly tear twice.

The different signs and unequal distances avoid a symmetrical “outline shadow”
effect. Shafts and bowls lose continuity at different heights from character to
character, creating the impression of a horizontal timing fault. This is a
static effect: repeated characters have identical drawings. There is no time
seed, Python `hash()` dependency, random generator, shader or alternate-glyph
shaping rule. Separate-process rebuilds with different Python hash seeds must
produce identical TTF and WOFF2 bytes.

## What is intentionally not glitched

Precomposed accented letters reuse the affected family's own letter body with
clean geometric accents. The normal dot is removed from accented lowercase `i`.
Supporting currency, fractions and certain symbols use the shared original
primitive recipes. Those auxiliary shapes are not subsequently torn.

Light box drawing, blocks and arrows are also intentionally clean. This
preserves their geometric meaning and stops a purely decorative treatment from
creating fake gaps in a box or reversing a direction. This does **not** qualify
the rest of Cache Rattle for operational interfaces. It simply places an explicit
boundary around the transformation. The clean auxiliary repertoire may contrast
with the heavily scanned ASCII; that contrast is accepted and documented, not
an accidental claim of a uniformly distressed international font.

## Artistic and utilitarian trade-offs

The useful constraint is predictability. A cover-art label can be rendered in a
browser, exported again later or placed on another machine without the
corruption changing its identity. The fixed cell is useful for intentionally
staged text grids and mock diagnostics. It is not an endorsement for long
terminal sessions.

The horizontal grooves and shifted strokes increase visual fragmentation. Small
sizes can turn grooves into grey texture and different screens may conceal or
exaggerate them. The initial 32–96 px trial range is aimed at seeing the effect,
not optimizing reading speed. The face has no manually optimized raster strikes
and makes no pixel-exact claim at any nominal size.

Never use this distortion as the sole carrier of important status, alarm,
credential or accessibility text. A fictional “memory error” title is an
appropriate use; a real low-battery warning or serial-number transcription
panel is not. There are no measured human-factor benefits and no claim that
people with any particular visual or reading condition will prefer it.

## Review and possible extensions

Rendered uppercase, lowercase, punctuation, accents and mixed alphanumeric
strings were inspected at multiple sizes. Automated checks enforce a complete
ASCII master, valid integer outlines, fixed advances, containment, nonempty
encoded glyphs and repeatable exported bytes. Rendering at 16/24/48 px verifies
that every nonspace glyph produces ink and that TTF/WOFF2 agree; it does not make
16 px a recommended reading size.

A later family extension could draw a separate restrained cut and compare it
with this one. It should not silently change the `v1` tear rule or add runtime
randomness to an installed font of the same version. Archive the present source
before changing the alphabet, so “cursed” remains an artistic property rather
than an excuse for an unreproducible build.
