# Gasket Sans — design notes

## Intent

A plain, proportional sans for interface labels, status lines and short prose
where the letters should read as machined, flat-cut parts. Angles are chosen so
that the shapes stay distinct without ornament.

## Construction

- Each glyph is a set of centre-line polylines (`M`/`L` only) in `source/design.py`,
  stroked at 64 units with flat ends and bevelled joins.
- Round letters (`C`, `D`, `O`, `Q`, `o`, `e` and similar) are octagonal. There are no
  Bézier curves in the master.
- Narrow glyphs (`i`, `l`, `!`, punctuation) use reduced advances. Any glyph whose ink
  would exceed its advance has the advance widened to ink plus 60 units, so no outline
  is clipped.
- Proportional spacing; no kerning beyond the shared Original Trio pair set.

## Practical intent (not measured)

- Short labels and status text at 14–18 px equivalent.
- Angular forms may help separate `0`/`O`, `1`/`l`/`I` and `5`/`S` at small sizes.

## Limits

- No reading-speed, fatigue or accessibility study has been run. The angular
  forms are a stylistic choice, not an accessibility claim.
- Some two-stroke glyphs (`&`, `%`, `@`, `$`) are compact approximations and are
  less refined than the letters.
- Outline proofs only. No Windows (DirectWrite/GDI) acceptance and no hinting.
- Authored without reference to any existing typeface's outlines.
