# Cantilever Shadow — design notes

## Intent

Heavy condensed capitals with a thin wireframe shadow behind.

## Construction

- Lineage: `CONDENSED`, a skeleton alphabet drawn for the Sixth Cohort and shared by several
  families; each family is a different construction treatment of it.
- CONDENSED stroked at 110 units; a 26-unit line copy of the skeleton is offset (+42, -42) and separated from the letter by a 10-unit gap. Glyphs that dip below -250 are compressed vertically.

## Practical intent (not measured)

- Display titles, 48 px and above.

## Limits

- The shadow adds width and clutter in small text; descenders are compressed.
- Sibling families on the same skeleton share letter structure; they are treatments, not
  independent alphabets.
- Outline proofs only: no hinting, Windows acceptance, legibility or accessibility study.
- Authored without reference to any existing typeface's outlines.
