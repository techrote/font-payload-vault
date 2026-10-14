# Girder Mono — design notes

## Intent

Fixed-pitch rectilinear monoline for terminals and listings.

## Construction

- Lineage: `BLOCK`, a skeleton alphabet drawn for the Sixth Cohort and shared by several
  families; each family is a different construction treatment of it.
- BLOCK stroked at 70 units, flat caps, mitred joins; every glyph is centred in a 620 cell. Punctuation reuses the CONDENSED skeletons widened 1.45x.

## Practical intent (not measured)

- Terminals and source listings, 12-18 px equivalent.

## Limits

- Distinguishing `0`/`O` and `1`/`l`/`I` relies on the slashed zero, serifed capital I and hooked l only; no ligatures; not tested in a terminal emulator.
- Sibling families on the same skeleton share letter structure; they are treatments, not
  independent alphabets.
- Outline proofs only: no hinting, Windows acceptance, legibility or accessibility study.
- Authored without reference to any existing typeface's outlines.
