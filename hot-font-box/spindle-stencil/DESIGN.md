# Spindle Stencil — design notes

## Intent

Heavy rounded stencil capitals for headlines and crate-style labels.

## Construction

- Lineage: `ROUND`, a skeleton alphabet drawn for the Sixth Cohort and shared by three
  families; each family is a different construction treatment of it, as in the Third Cohort.
- Round skeleton stroked at 132 units, with 34-unit horizontal bridge cuts at mid height in `C D G J O Q S U 0 6 8 9` and in lowercase `b c d g o p q s u`.

## Practical intent (not measured)

- Display sizes (about 40 px and above).

## Limits

- Bridge cuts weaken `O`/`Q`/`0` recognition at small sizes; letters with crossbars are left uncut so the stencil effect is not uniform.
- Sibling families on the same skeleton share letter structure; they are treatments, not
  independent alphabets.
- Outline proofs only: no hinting, Windows acceptance, legibility or accessibility study.
- Authored without reference to any existing typeface's outlines.
