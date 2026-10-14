# Quantum Step — design notes

## Intent

Round skeleton snapped to a 60-unit grid so curves become stair-steps.

## Construction

- Lineage: `ROUND`, a skeleton alphabet drawn for the Sixth Cohort and shared by several
  families; each family is a different construction treatment of it.
- ROUND stroked at 92 units, then vertices are snapped with `set_precision(60)`; invalid results are repaired with a zero buffer.

## Practical intent (not measured)

- Titles and retro labels, 32 px and above.

## Limits

- Snapping can collapse small counters, and stepping is uneven on diagonals.
- Sibling families on the same skeleton share letter structure; they are treatments, not
  independent alphabets.
- Outline proofs only: no hinting, Windows acceptance, legibility or accessibility study.
- Authored without reference to any existing typeface's outlines.
