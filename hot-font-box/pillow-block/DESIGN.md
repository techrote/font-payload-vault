# Pillow Block — design notes

## Intent

Very heavy rectilinear letters with softened convex corners, for posters.

## Construction

- Lineage: `BLOCK`, a skeleton alphabet drawn for the Sixth Cohort and shared by several
  families; each family is a different construction treatment of it.
- BLOCK stroked at 150 units, then morphologically opened by 36 units (erode then dilate with round joins) so convex corners round while concave corners stay sharp. Punctuation reuses CONDENSED skeletons widened 1.45x.

## Practical intent (not measured)

- Large titles, 56 px and above.

## Limits

- Counters nearly close in `B 8 e a`; the opening also rounds terminals, so letters look softer than the rectilinear skeleton suggests.
- Sibling families on the same skeleton share letter structure; they are treatments, not
  independent alphabets.
- Outline proofs only: no hinting, Windows acceptance, legibility or accessibility study.
- Authored without reference to any existing typeface's outlines.
