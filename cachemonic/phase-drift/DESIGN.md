# Phase Drift — design notes

## Intent

An experimental raster face for fictional readouts, scanned-dot labels and
deliberately unsettled signage. The grid is visible on purpose.

## Construction

- Every glyph is a 5×7 bitmap written as literal rows in `source/design.py`.
- Each lit cell is a 40-unit-radius disc on a 90 × 100 unit pitch, so dots keep
  a visible gap rather than merging into bars.
- Row phase: rows 0–6 are displaced by `DRIFT = (0, 16, -10, 24, -14, 8, -4)`
  units. The displacement is fixed, not random, so builds are reproducible.
- Caps only: lowercase input uses the capital raster. The x-height and cap-height
  are both 680 units.
- Fixed pitch; the 600-unit advance keeps all drifted dots inside the cell.

## Practical intent (not measured)

- Short labels, codes and decorative fictional readouts at 24 px and above.
- Not for body text or any content where a letter must be identified reliably.

## Limits

- Five-by-seven rasters are ambiguous for several pairs (`8`/`B`, `O`/`0`, `Q`/`O`,
  `5`/`S`). Readability is not established for any of them.
- Row drift is a visual device; at small sizes it reads as jitter.
- Punctuation rasters are approximate.
- Outline proofs only. No Windows acceptance, no hinting, no print test.
- Authored without reference to any existing typeface's outlines or to the other
  cachemonic rasters.
