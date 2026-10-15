# Gravel Grit — design notes

## Intent

Heavy round letters pitted by deterministic grit holes.

## Construction

- Lineage: `ROUND`, a skeleton alphabet drawn for the Sixth Cohort and shared by several
  families; each family is a different construction treatment of it.
- ROUND stroked at 130 units; 34 holes per glyph (radius 7-19) are placed with a random generator seeded by the character code, so builds are reproducible.

## Practical intent (not measured)

- Titles and fictional labels, 48 px and above.

## Limits

- Holes are not positioned for legibility and may nick thin parts; the look differs per glyph.
- Sibling families on the same skeleton share letter structure; they are treatments, not
  independent alphabets.
- Outline proofs only: no hinting, Windows acceptance, legibility or accessibility study.
- Authored without reference to any existing typeface's outlines.
