# Original Trio — production and verification workflow

**Scope:** Latchline Mono, Diecast Relay and Cache Rattle, version 1.000.
Their three font folders, shared `tools/original_trio` code and Original Trio
documentation are new OFL-licensed Font Software. This work does not relicense,
rebuild, replace or claim authorship of Knurled Swarf or the existing idea archive.

![The three original faces](original-trio-overview.svg)

## Authority and provenance

The repository was inspected at `a390824e105bc3fb3b02f042e2b2937401244996`
(`main`, merge of PR #2). There was no root README, CI workflow or open PR at the
initial inspection. Inspiration came from the category READMEs, Knurled Swarf's
README/WORKFLOW and the theme/name discussion in
[`subfolder-name-ideadump-refonly.md`](subfolder-name-ideadump-refonly.md).

The useful themes were machinist vocabulary, cybernetic interfaces, a distinction
between useful console text and deliberate visual derangement, and preserving
complete rebuildable sources. **No existing font file or original glyph master
was used as design input.** These are newly authored AI-assisted procedural
letterforms, not traced, renamed, remapped or filtered versions of another font.
This is a provenance statement about this creation process, not an assertion
that elementary letter shapes cannot resemble earlier type design.

| Family | Independent design source | Intended home |
|---|---|---|
| Latchline Mono | Authored centre-line paths, strokes and optical lowercase | `cmd-font-container/latchline-mono` |
| Diecast Relay | Authored solid/counter polygons, relief slots and small capitals | `hot-font-box/diecast-relay` |
| Cache Rattle | Authored seven-column ASCII bitmaps and deterministic row drift | `cachemonic/cache-rattle` |

Only serialization, original auxiliary-symbol recipes, repertoire, licence and
proof tooling are shared. A common exporter does not make these three weights
of the same underlying font.

## Source layout

Each family has `source/design.py`, `README.md`, `DESIGN.md`, `OFL.txt`, two
compiled files in `fonts/`, and a `specimen/` folder containing a path-only SVG
proof, a complete character-map SVG and an offline HTML tester. Sources are plain
Python and literal paths/grids. No GUI font editor or external design asset is
required to rebuild them.

Shared tooling:

| File | Responsibility |
|---|---|
| `geometry.py` | Original stroke/polygon primitives, unions, integer quantization and deterministic contour ordering |
| `repertoire.py` | Exact 254-character allowlist, accents, symbols and cell geometry; missing mappings fail the build |
| `build.py` | TrueType and WOFF2 serialization, metrics/naming/GPOS, checksummed output manifest |
| `verify.py` | Structural, geometric, FreeType, OTS and independent-process reproducibility tests |
| `specimen.py` | Original outline proofs, full glyph maps and local browser testers; `--check` detects stale outputs |
| `browser_smoke.py` | Chromium font loading, tester controls, fallback warnings and no-external-request checks |

## Rebuild

Use Python **3.11 or later** and the pinned dependencies at the repository root.
GitHub CI uses Python 3.12 and Ubuntu 24.04. On Linux, FreeType must be available;
the hosted workflow installs `libfreetype6` and `opentype-sanitizer`.

```sh
python -m venv .venv
# Activate the environment using your shell's usual activation command.
python -m pip install -r requirements-original-trio.txt
python tools/original_trio/build.py
python tools/original_trio/verify.py --require-ots
python tools/original_trio/specimen.py
python tools/original_trio/specimen.py --check
```

Where OTS is not installed, omit `--require-ots` for local development only. The
sanitizer test will be explicitly **skipped**, not passed. Hosted acceptance
requires it and fails if the executable is unavailable. `build.py --output DIR`
rebuilds into a separate directory without modifying the master files.

Commit changed sources and generated files together. Do not edit a compiled TTF,
WOFF2, SVG or manifest as the authoritative design. A master revision invalidates
its old proof sheets and binary evidence even if the filename stays the same.

## Outline and font production

The construction uses Shapely unions/differences and explicit path sampling.
Valid polygons are snapped to integer font units, normalized, consistently
oriented and given canonical starting points. Exterior contours are clockwise;
interior counters are counterclockwise. FontTools constructs a fresh TrueType
font with `glyf` outlines and wraps it as WOFF2 using Brotli.

All three use 1000 units/em, `hhea` and typographic ascender/descent of 1000/−250,
zero extra line gap, matching Windows clipping extents and OS/2 version 4 with
`USE_TYPO_METRICS`. Name records, version, licence and fixed-pitch metadata are
explicit. Every encoded scalar has its own mapping; `.notdef` is visible. There
are no zero-width combining marks, GSUB substitutions, programming ligatures,
variable axes, bitmap strikes or TrueType hint instructions. Diecast alone has
the small declared GPOS kerning set.

The timestamp is fixed at 2026-10-14 00:00:00 UTC. Family/glyph ordering and
Cache Rattle's SHA-256 phase are deterministic. Reproducibility is checked with
separate Python processes and different hash seeds. This establishes repeatable
bytes for the pinned build environment; it is not a claim that different GEOS,
FontTools, Brotli versions or every operating system yield identical bytes.

`docs/original-trio-manifest.json` contains byte sizes and SHA-256 values for all
six compiled outputs. The hosted build produces those font files directly from
the committed sources; no host-installed fonts are packaged.

## What the tests establish

The twelve test groups check exact cmap coverage and nonempty glyphs; every
quantized contour against both exports; names, bounds, metrics and independent
master identities; FreeType rendering; confusable distinctions and selected
counters in Latchline; accent-dot replacement; box/block geometry; Diecast
spacing, small capitals and kerning; separate-process reproducibility; and OTS.

FreeType renders each of 254 characters at 16, 24 and 48 px in each family,
comparing the desktop TTF against the decoded WOFF2. This gives **2,286 paired
raster comparisons**. All nonspace characters must produce ink, but the test
does not claim they are equally legible at those sizes. Latchline's extra
confusable and counter tests are narrow regression checks, not human-factors
research. SVG proofs are generated from source outlines and are reviewed
alongside the raster output, not substituted for it.

The browser tester uses only local font URLs and system UI labels. It uses
`textContent` for user text, has no external libraries or telemetry, reports
missing codepoints and visibly reports a font-loading failure. Serve the repo
with `python -m http.server 8000` where local-file font access is restricted,
then open the relevant `specimen/index.html` through that server.

The optional local browser test (required in CI) is:

```sh
python -m pip install -r requirements-original-trio-browser.txt
python -m playwright install chromium
python tools/original_trio/browser_smoke.py
```

CI installs the Chromium system dependencies as well. It checks that all three
fonts load, all 254 character cells exist, size/line-height/tracking/kerning and
polarity controls work, unsupported Unicode is reported, user input stays literal
text rather than becoming HTML, and failed font requests produce a visible warning.
It also rejects requests outside its loopback test server. This is browser smoke
coverage, not a user study or a cross-browser compatibility certificate.
The initial hosted result is saved in
[`original-trio-browser-verification.json`](original-trio-browser-verification.json).

Normal CI validates the **checked-in** font files; it does not first regenerate
them and thereby conceal stale outputs. Specimens are checked the same way.
Current CI results belong to their exact commit. The checked-in
[`original-trio-verification.json`](original-trio-verification.json) records the
initial hosted qualification and embeds the exact compiled-font manifest.

## Review corrections and limits

The first visual/structural review found and corrected a too-similar Diecast
D/O pair, dot stacking on accented lowercase i, an asymmetric Cache Rattle
closing brace, an inverted question mark below the declared descender, and
OS/2 version/flag consistency. The tests retain the relevant invariants instead
of weakening bounds to accept the defects.

These remain first releases with one style each. There is no Windows installation
acceptance, DirectWrite/GDI comparison, print-distance test, physical stencil
qualification or measured accessibility/fatigue/reading-speed result. Declared
size ranges and practical benefits are intentions. Display faces are not
appropriate substitutes for dependable operational text. Each DESIGN.md spells
out its own trade-offs and exclusions.

## Technical references

These references explain the tools/formats, not the source of the artwork:

- [FontTools FontBuilder source and construction example](https://github.com/fonttools/fonttools/blob/main/Lib/fontTools/fontBuilder.py)
- [FontTools TrueType/WOFF2 tooling](https://fonttools.readthedocs.io/en/latest/ttx.html)
- [Shapely buffer construction and join/cap behavior](https://shapely.readthedocs.io/en/stable/reference/shapely.buffer.html)
- [OpenType horizontal metrics specification](https://learn.microsoft.com/en-us/typography/opentype/spec/hmtx)
- [Open Font License official text](https://openfontlicense.org/open-font-license-official-text/)

The included OFL applies only to the explicitly identified new Font Software.
Dependencies remain under their upstream licences and are installed, not vendored.
