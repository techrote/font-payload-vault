# Ingot Shadow — design notes

## Intent

Heavy condensed capitals with a stepped drop shadow.

## Construction

- Lineage: `CONDENSED`, a skeleton alphabet drawn for the Sixth Cohort and shared by several
  families; each family is a different construction treatment of it.
- CONDENSED stroked at 100 units; seven copies offset (+4, -4) each form the shadow, separated from the letter by a 12-unit gap. Glyphs that dip below -250 are compressed vertically.

## Practical intent (not measured)

- Display titles, 40 px and above.

## Limits

- The shadow adds clutter and visual width in small text.
- Sibling families on the same skeleton share letter structure; they are treatments, not
  independent alphabets.
- Outline proofs only: no hinting, Windows acceptance, legibility or accessibility study.
- Authored without reference to any existing typeface's outlines.
