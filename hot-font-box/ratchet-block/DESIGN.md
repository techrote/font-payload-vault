# Ratchet Block — design notes

## Intent

A heavy, compact display face for headlines and labels that must be read from
across a room: loud, blocky and deliberately mechanical.

## Construction

- Uppercase skeletons in `source/design.py` are centre-line polylines stroked at
  120 units with bevelled joins. Counters are kept open rather than filled.
- Lowercase codepoints reuse the capital outline scaled to 74 % width and 66 %
  height, sitting on the baseline. This is a small-capital convention; the
  character map shows the same glyph for both cases.
- Digits and punctuation share the same stroke weight and monospaced 600-unit cell.
- One style only; no weight axis.

## Practical intent (not measured)

- Titles and short labels at display sizes (roughly 36 px and above).
- Not for body text, long captions or dense tables.

## Limits

- Lowercase is not text lowercase; `a` and `A` are visibly different only in size.
- Heavy strokes close the counters of `B`, `P`, `R`, `8` and `@` at very small sizes.
- Some punctuation (`@`, `$`, `&`, `%`) is simplified.
- Outline proofs only. No Windows acceptance, no hinting, no print-distance test.
- Authored without reference to any existing typeface's outlines.
