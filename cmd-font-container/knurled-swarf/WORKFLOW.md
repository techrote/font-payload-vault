# Knurled Swarf: how it's built

The whole font is plain text plus Python. Edit a grid, rerun the build, and every format regenerates and is re-verified.

```
source/m5.txt, m7.txt          hand-drawn masters (the real design)
source/m6/m9/m10/m11.over.txt  hand-drawn fixes for derived masters
        │
        ▼  swarf.py   parse → derive in-between masters → assemble per-size cells
        │             → compose accents → generate box drawing/blocks → bold
        ▼  build.py   TTF (outlines + EBDT/EBLC strikes + hdmx), per-size TTF, WOFF2, FON, BDF
        ▼  verify.py  FreeType renders every glyph of every file; must match the source bitmaps exactly
        ▼  specimen.py / make_tester.py   PNG sheets + self-contained HTML type tester
```

## 1. Masters

A **master** is one complete design at one cap height. Only two are drawn by hand from scratch:

| master | cap | x-height | descender | widths | origin |
|---|---|---|---|---|---|
| M5 | 5 | 4 | 1 | caps ~3 | hand (`m5.txt`) |
| M6 | 6 | 4 | 2 | = M5 | derived from M5 + `m6.over.txt` |
| M7 | 7 | 5 | 2 | caps 5, lower 4 | hand (`m7.txt`) |
| M8 | 8 | 6 | 2 | = M7 | derived from M7 |
| M9 | 9 | 7 | 3 | +1 column | derived from M7 + `m9.over.txt` |
| M10 | 10 | 7 | 3 | +1 column | derived from M7 + `m10.over.txt` |
| M11 | 11 | 8 | 3 | +2 columns | derived from M7 + `m11.over.txt` (all diagonal glyphs hand-drawn) |

Each pixel size maps to a master plus line spacing (`SIZES` in `swarf.py`). The cell height always equals the px size:

| px | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| master | M5 | M5 | M6 | M6 | M7 | M8 | M8 | M9 | M10 | M10 | M11 |
| ascent / descent | 5/1 | 6/1 | 6/2 | 7/2 | 8/2 | 9/2 | 10/2 | 10/3 | 11/3 | 12/3 | 13/3 |

### Grid file format

```
@ A                 header: "@ " + the character (or U+XXXX, or "space w=2")
.###.               rows start at the top of the cap height
#...#               '#' = ink, '.' = empty
#####               trailing descender rows may be left out
```

Optional header hints steer the derivation of bigger masters:

| hint | meaning |
|---|---|
| `mode=lower` / `mode=cap` | stretch inside the x-height region (lowercase, math symbols) or the cap region |
| `yc=3` | when adding rows to the cap region, duplicate source row 3 |
| `yx=4` / `ya=t` / `yd=b` | same for x-height / ascender / descender regions; `t`/`b` = insert a blank row at top/bottom |
| `xw=1,3` | when widening, duplicate source columns 1 then 3 |
| `wc=2` | widen by this many columns (overrides the master default) |
| `yc.M9=2,4` | any hint can be limited to one target master with a `.Mn` suffix |

Without hints, the engine picks the "quietest" row or column to duplicate: single-pixel stems, never bars. It keeps symmetric glyphs
symmetric and never doubles a 1px stem or dot. Anything that still looks wrong goes in the master's `.over.txt` file, drawn at that
master's full size.

## 2. Per-size assembly (`swarf.py`)

- **Accents** (À…ÿ, Š Ž Ÿ): composed per size. An accent goes above the letter with a 1px gap if there's room. Otherwise it touches.
  If even that won't fit (e.g. capitals at 6px), the letter is squashed by removing its most redundant row.
- **Ø ø Ð ı ç Ç**: overlays and derived shapes.
- **Box drawing / blocks / shades**: generated to fill the exact cell (width = digit advance, height = px size), so they tile seamlessly.
  The junction rules for single/double lines are in `box_glyph()`.
- **Math symbols** (`- + = × ÷ < > ~ …`) are re-centred on the x-height in every master.
- **Bold**: every 1px gap between strokes is widened to 2px first, then the glyph is smeared 1px to the right (VGA / Win 3.x System
  style). Counters therefore never clog. Box drawing and geometric shapes are not emboldened.

## 3. Export (`build.py`)

- **Universal TTF**: outlines are the 10px design traced into pixel-square polygons (UPM 1280, 128 units per pixel). Every size
  6–16 is stored as an embedded bitmap strike (EBDT/EBLC, written byte-by-byte in `build_strikes()`), with an `hdmx` table carrying
  the per-size advances. `gasp` turns off smoothing so edges stay hard.
- **Per-size TTF**: UPM = N × 128, so at N px every outline edge lands exactly on a pixel boundary. Each one also carries its own strike.
- **FON**: a 16-bit NE font library holding 11 FNT v2 raster resources (one per size), cp1252 encoding (`make_fnt` / `make_fon`).
- **BDF**: one file per size and weight.
- **WOFF2**: the per-size TTFs, compressed.

## 4. Verification (`verify.py`)

For each weight, FreeType renders every glyph from:
the universal TTF's 11 strikes, the universal outline at 10px, every per-size TTF (outline in mono mode, outline anti-aliased, and its strike),
and all 11 faces of the FON. Bitmap, bearings and advance must match the source exactly, and anti-aliased renders must contain
**zero** grey pixels. Expected output: `ALL OK` (112 checks).

## 5. Review tools

| script | use |
|---|---|
| `python dump.py 13 "AKMN"` | print glyphs at a size as text grids (the fastest way to review a fix) |
| `python preview.py 6,10,16 reg 4` | PNG sheets per size into `../preview/` (git-ignored) |
| `python specimen.py` | the specimen PNGs in `../specimen/` |
| `python make_tester.py` | `../specimen/specimen.html`, the offline type tester with every per-size font embedded |

## Typical edit loop

1. Change a glyph in `m7.txt` (or add an override in `m11.over.txt`).
2. `python dump.py 16 "<chars>"` to look at the result at every affected size.
3. `python build.py && python verify.py` → expect `ALL OK`.
4. `python specimen.py && python make_tester.py`, then commit sources and outputs together.
