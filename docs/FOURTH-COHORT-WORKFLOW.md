# Fourth Cohort — production workflow

**Scope:** Gasket Sans, Ratchet Block and Phase Drift, version 1.000. Their three
font folders, `tools/fourth_cohort/cohort.py` and this document are new
OFL-licensed Font Software.

## Provenance

The three designs are newly authored procedural masters: centre-line polylines
(Gasket Sans, Ratchet Block) or 5×7 dot rasters (Phase Drift). No existing font
file, glyph outline or traced image was used as input. The shared Original Trio
code supplies only serialization, the repertoire extension for accents and
symbols, geometry primitives and the composite-glyph rules.

## Rebuild

Requires Python 3.11+ and the pinned Original Trio dependencies:

```sh
python -m pip install -r requirements-original-trio.txt
python tools/fourth_cohort/cohort.py
```

`cohort.py --proofs-only` regenerates specimens and testers from the committed
fonts' sources without rewriting the binaries. `cohort.py --output DIR` writes into
another directory and leaves the sources unchanged.

## Checks performed for this release

- Every family has 254 encoded characters, identical cmap in TTF and WOFF2, and a
  visible `.notdef`.
- Every glyph's ink lies within `0..advance` horizontally and `-250..1000`
  vertically.
- Gasket Sans is proportional; Ratchet Block and Phase Drift are fixed pitch.
- Lowercase in Ratchet Block and Phase Drift is intentionally small-cap or caps
  input, not text lowercase.
- Rendered and reviewed as a FreeType preview at 56 px.

## Not yet done

- The Original Trio verification suite (`tools/original_trio/verify.py`) and its
  browser smoke test are not extended to these families, and no CI workflow was
  added for them. Their FreeType, OTS and reproducibility checks have not been run.
- No Windows installation or DirectWrite/GDI acceptance, no hinting, no legibility
  or accessibility study.
