# Raster Forge — design / construction record

## Artistic brief

**A joined chunky pixel alphabet with asymmetric extrusion tongues.** This typeface belongs to [`hot-font-box/`](../), the vault's workshop display compartment.

Imagine a robotic foundry extruding molten square sections through a stamping die.

## How it is made

Hand-authored seven-column matrix rows become thick, bevelled tiles. On selected exposed right edges, a shorter block tongue extends toward the next cell. Unioned tiles create dense modular letter bodies rather than dotted halos or an enlarged screenshot.

The editable **family configuration and deliberate glyph corrections** are in [`source/design.py`](source/design.py). The full independently drawn **grid lettering lineage** lives in [`tools/third_cohort/masters.py`](../../tools/third_cohort/masters.py), alongside three other original alphabets. Each lineage has independently authored uppercase, genuine lowercase and ten numerals. Three named faces in this cohort share each base alphabet but use separate construction algorithms and local glyph overrides: **they are distinct typeface treatments, not twelve unrelated hand-drawn alphabets**. Shared new ASCII punctuation and auxiliary recipes are identified in the central workflow; no older vault font is traced or transformed.

The forge mode has a nominal primary feature width of **100 font units**, an initial advance limit of **770 units**, and fixed pitch across all codepoints. The style metadata is **Regular**, with a 1000-unit em and 1000/−250 ascent/descent line metrics. All contours are serialized deterministically to integer TrueType coordinates; curves are sampled into polygon segments. There are no imported artwork paths, raster screenshots or proprietary font dependencies.

## Ergonomic or utilitarian intent

Large arcade-industrial banners, splash text, title cards and deliberately blocky numerals. Suggested first trial: **40–105 px**. This is a design intention, **not measured reading-speed, fatigue, dyslexia, error-rate or accessibility performance**.

The identity of common `I/l/1/|`, `O/0`, `B/8`, `g/q` groupings and accented letters can be inspected in the full 254-codepoint map and editable local type tester. Some display and experimental faces deliberately trade those distinctions for a specific texture, so their suitability must be judged at actual output resolution and in context.

## Limits, reuse, next work

The extrusions are optical, not supported machine extrusion geometry. It remains a scalability-first outline with no size-specific pixel strikes.

Each 1.000 release has one named style (no variable axes), **254 encoded codepoints and 255 glyph records including `.notdef`**, and ships as a standard TTF and WOFF2. Unicode scope: printable ASCII, Latin-1, selected Windows-1252 characters, arrows, arithmetic marks, light box-drawing and blocks. Precomposed accents are assembled from this design's bodies; some supporting neutral symbols are shared across the twelve fonts. General non-Latin scripts, arbitrary combining sequences, Nerd Fonts and Powerline glyphs are not provided.

There are no native hinting instructions, embedded bitmap strikes, kerning or ligature shaping in version 1.000. Browser testing is limited to hosted Chromium; native Windows GDI/DirectWrite/ClearType behavior and physical-pixel use have not been accepted. No stencil, fabrication or safety-signage qualification is asserted. Rebuild using the root workflow, and inspect visual/functional changes before publishing another version. The new source, binaries and documentation are under **SIL OFL 1.1**; this does not change any earlier vault licensing.
