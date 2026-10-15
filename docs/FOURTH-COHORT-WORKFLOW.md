# Fourth Cohort — production workflow

**Scope:** Gasket Sans, Ratchet Block and Phase Drift, version 1.100 (remastered from 1.000). Their three
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

## 1.100 remaster

Found in the 1.000 render and changed:

- **Gasket Sans:** letters touched (no side bearings) and punctuation dots were
  thin slivers. Spacing is now ink-fitted with 72-unit bearings, figures are tabular
  in a 600 cell, and `. , : ; ! ? i j` use square dots matching the stem. `%` redrawn.
- **Ratchet Block:** cell widened 600 to 660 with centred ink, small capitals enlarged
  (86 % x 78 %, x-height 546), dots are full-weight squares, `%` redrawn.
- **Phase Drift:** dots enlarged (radius 40 to 43), drift widened, ink centred.
- Version, name table and `head.fontRevision` are 1.100. `render.py` produces the
  proof image in the README.

## Verification (Fourth and Sixth Cohorts)

`tools/fourth_cohort/verify.py --cohort fourth|sixth --require-ots` ports the
family-independent Original Trio checks: exact 254-character repertoire, outlines
equal to the quantized master, metrics and bounds, names, FreeType TTF-versus-WOFF2
raster parity at 16, 24 and 48 px, OTS on every TTF and WOFF2, and rebuilds under two
hash seeds that must equal the committed bytes. The Latchline- and Diecast-specific
tests do not apply. `.github/workflows/fourth-sixth-cohorts.yml` runs it on Ubuntu 24.04
with OTS required, for both cohorts, and uploads an Ubuntu build as an artifact.

Results at commit `44c925f`:

- **Original Trio suite** (`tools/original_trio/verify.py --require-ots`): 12 tests pass,
  including OTS. It covers only the original three families.
- **CI:** both cohorts pass on Ubuntu 24.04 (all 7 tests, OTS required).
- **Windows 11, GDI+:** all 39 TTFs load from a private font collection (no installation)
  and render; see `docs/windows-gdi-render.png`.
- **Windows 11, Chromium (DirectWrite):** all 39 WOFF2 files load through the FontFace API and
  five offline testers report all characters present. Visual inspection was not scripted.

**Byte reproducibility is per operating system.** Seven curve-based families (Lathe Round, Slip
Echo, Skiff Slant, Pebble Bold, Contour Ripple, Wave Warp, Gravel Grit) rebuild a unit or two
differently on Windows than on Linux, so their committed fonts, SVG proofs and the Sixth
manifest come from the hosted Ubuntu build. Running `verify.py` on Windows therefore reports
stale-output failures for those seven; the Ubuntu CI run is the reference.

## Not yet done

- No installed-font Windows test (fonts were loaded privately, not installed), no
  DirectWrite/GDI hinting comparison, and no automated browser smoke test like the
  Original Trio's (the testers were checked with a script, not a test suite).
- No legibility or accessibility study. In the heavy condensed families the single-storey
  `a` is easy to read as `o` at small sizes.
