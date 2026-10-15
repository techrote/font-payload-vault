# Plinth Mono — design notes

## Intent

Fixed-pitch slab serif for listings and typewriter-style text.

## Construction

- Lineage: `SLAB`, a skeleton alphabet drawn for the Sixth Cohort and shared by several
  families; each family is a different construction treatment of it.
- SLAB stroked at 64 units, flat caps, mitred joins; every glyph centred in a 700 cell. Figures 2-9 and punctuation reuse the ROUND skeletons.

## Practical intent (not measured)

- Listings and typewriter-style text, 12-20 px equivalent.

## Limits

- Wide cell wastes width for narrow letters; `0`/`O` distinguished only by the slash; not tested in a terminal emulator.
- Sibling families on the same skeleton share letter structure; they are treatments, not
  independent alphabets.
- Outline proofs only: no hinting, Windows acceptance, legibility or accessibility study.
- Authored without reference to any existing typeface's outlines.
