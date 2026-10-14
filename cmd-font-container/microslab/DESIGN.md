# Microslab — design / construction record

## Artistic brief

**A detented, squared-off typewriter grid with selective slab terminals.** This typeface belongs to [`cmd-font-container/`](../), the vault's terminal and system-interface compartment.

Read like a small machined type slug: a hard mechanical register, not a nostalgic pre-existing slab-serif revival.

## How it is made

Angular centre lines are drawn independently of the rounded grammar. Square stems receive narrow rectangular serif feet only at explicitly eligible horizontal terminals; diagonals and tight round counters are protected. The zero carries a central dot rather than a slash.

The editable **family configuration and deliberate glyph corrections** are in [`source/design.py`](source/design.py). The full independently drawn **micro lettering lineage** lives in [`tools/third_cohort/masters.py`](../../tools/third_cohort/masters.py), alongside three other original alphabets. Each lineage has independently authored uppercase, genuine lowercase and ten numerals. Three named faces in this cohort share each base alphabet but use separate construction algorithms and local glyph overrides: **they are distinct typeface treatments, not twelve unrelated hand-drawn alphabets**. Shared new ASCII punctuation and auxiliary recipes are identified in the central workflow; no older vault font is traced or transformed.

The slab mode has a nominal primary feature width of **82 font units**, an initial advance limit of **760 units**, and fixed pitch across all codepoints. The style metadata is **Regular**, with a 1000-unit em and 1000/−250 ascent/descent line metrics. All contours are serialized deterministically to integer TrueType coordinates; curves are sampled into polygon segments. There are no imported artwork paths, raster screenshots or proprietary font dependencies.

## Ergonomic or utilitarian intent

Monospaced calibration tables, terminal panes, machine inventories and printed labels where fixed columns matter. Suggested first trial: **20–32 px**. This is a design intention, **not measured reading-speed, fatigue, dyslexia, error-rate or accessibility performance**.

The identity of common `I/l/1/|`, `O/0`, `B/8`, `g/q` groupings and accented letters can be inspected in the full 254-codepoint map and editable local type tester. Some display and experimental faces deliberately trade those distinctions for a specific texture, so their suitability must be judged at actual output resolution and in context.

## Limits, reuse, next work

Slabs add density; evaluation at the actual monitor scale is essential. It lacks native Windows GDI validation and optimized raster strikes.

Each 1.000 release has one named style (no variable axes), **254 encoded codepoints and 255 glyph records including `.notdef`**, and ships as a standard TTF and WOFF2. Unicode scope: printable ASCII, Latin-1, selected Windows-1252 characters, arrows, arithmetic marks, light box-drawing and blocks. Precomposed accents are assembled from this design's bodies; some supporting neutral symbols are shared across the twelve fonts. General non-Latin scripts, arbitrary combining sequences, Nerd Fonts and Powerline glyphs are not provided.

There are no native hinting instructions, embedded bitmap strikes, kerning or ligature shaping in version 1.000. Browser testing is limited to hosted Chromium; native Windows GDI/DirectWrite/ClearType behavior and physical-pixel use have not been accepted. No stencil, fabrication or safety-signage qualification is asserted. Rebuild using the root workflow, and inspect visual/functional changes before publishing another version. The new source, binaries and documentation are under **SIL OFL 1.1**; this does not change any earlier vault licensing.
