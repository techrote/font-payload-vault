# Third Cohort / 03 — twelve procedural typefaces

This publication adds twelve distinct faces alongside the repository's existing
Knurled Swarf, Original Trio and Workshop Six collections. It does not replace
any existing family or retire any previous files. At kickoff the canonical
`main` base was `7eed6b3abea1db4e1e3587b9c9df1c740a642d7f`, with no open PRs;
the previous six-font exact-main CI had passed.

![All twelve new faces](third-cohort-overview.svg)

## Design register

| Category | Family | Construction | Primary design intention |
|---|---|---|---|
| System | [Tracebar Mono](../cmd-font-container/tracebar-mono/) | Wired monoline strokes | Literal terminal and instrumentation text |
| System | [Bushing Sans](../cmd-font-container/bushing-sans/) | Independently drawn rounded open curves | Proportional UI labels with tabular digits |
| System | [Microslab](../cmd-font-container/microslab/) | Angular routing and selected mechanical slab ends | Fixed-pitch records |
| System | [Nibble Nine](../cmd-font-container/nibble-nine/) | Original 7×9 bitmap master, rectangle outlines | Visible controller-cell rhythm |
| Display | [Torque Plate](../hot-font-box/torque-plate/) | Thick mechanical stock and occasional rivet holes | Heavy machine nameplates |
| Display | [Sling Arc](../hot-font-box/sling-arc/) | Rounded tubes and true Oblique shear | Forward-leaning titles |
| Display | [Swarf Bridge](../hot-font-box/swarf-bridge/) | Boolean hollow welded-outline silhouette | Framed display lettering |
| Display | [Raster Forge](../hot-font-box/raster-forge/) | Overlapping bevelled modules with extruded tongues | Blocky industrial headlines |
| Experiment | [Shift Ghost](../cachemonic/shift-ghost/) | Separated offset imprints | Double-register defect |
| Experiment | [Eddy Notch](../cachemonic/eddy-notch/) | Deterministically drilled rounded heavy letters | Test-apparatus voids |
| Experiment | [Carbon Check](../cachemonic/carbon-check/) | Mechanical stock with diagonal subtractive slits | Machining chatter and corrosion |
| Experiment | [Checksum Haze](../cachemonic/checksum-haze/) | Pixel nodes with seeded satellite debris | Faint digital signal texture |

## The provenance boundary is deliberate

These are **twelve distinct delivered typefaces derived from four new, original,
independently drawn Latin alphabet lineages**, not twelve separately hand-lettered
alphabets. All four bases are authored in `tools/third_cohort/masters.py`, with
62 distinct uppercase/lowercase/digit drawings per base. `TRACE`, `BUSHING` and
`MICRO` are independent polyline collections; `GRID` is an independently
hand-entered 62-character 7×9 bitmap collection. Each face has its own
`source/design.py` defining the treatment, geometry, cell/advance rules, target
use, style metadata and individual glyph corrections. `create_specs.py` records
the face-specific rationale and can regenerate the family docs and configs.

No compiled or installed pre-existing font is a design input. In particular,
none of Knurled Swarf's grids or any of the previous nine families' Latin outlines
was copied, traced, aliased, renamed, or run through a weight/distortion filter.
Reusable Unicode accent recipes and punctuation are **new common construction
utilities** for this cohort; they are explicitly not twelve independent
optically drawn international alphabets. Basic arithmetic, light box drawing,
blocks and selected geometric symbols retain shared neutral geometry across
all twelve faces. This reuse is important for honest documentation.

## Glyph geometry and export contract

Font units: UPM 1000, typographic ascent 1000, descent −250, zero extra line gap.
All glyph data is baked into deterministic quadratic-free TrueType polygons;
round forms are sampled and flattened to straight line segments, then normalized
and rounded to integer font units. `FontBuilder` assembles `glyf`, `hmtx`, `cmap`,
`OS/2`, `name`, `post`, `head`, and `gasp`; WOFF2 uses the same outlines.
Build timestamps and ordering are fixed for bit-reproducibility.

- Every family has 254 mapped codepoints (95 printable ASCII, 96 Latin-1,
  27 additional Windows-1252 punctuation, 36 selected arrows/math/box/blocks
  after deduplicating codepoints); plus `.notdef` gives 255 glyph records.
- Capitals, **real lowercase**, ten figures and ASCII punctuation are present.
  Accents are composed from these bodies and original neutral mark recipes.
  Not all auxiliary marks follow experimental distress treatments.
- Monospaced fonts set `post.isFixedPitch` and use exactly one advance for every
  encoded character, including control-style box/blocks and whitespace.
  Proportional fonts use width-dependent letter advances and equal tabular
  advances for all ten figures.
- `Sling Arc` has a real **Oblique** style: slant in the outline, consistent
  `post.italicAngle`, OS/2 selection flags, head macStyle and caret slope.
  The other eleven styles are independently labelled Regular.
- The functional light box/blocks intentionally touch logical cell boundaries.
  Raster seams can still arise from app line height, scaling and fallback.

### Rebuild locally

Python 3.12 and the existing pinned production packages:

```sh
python -m pip install -r requirements-third-cohort.txt
python tools/third_cohort/build.py
python tools/third_cohort/verify.py
python tools/third_cohort/specimen.py
python tools/third_cohort/specimen.py --check
python tools/third_cohort/browser_smoke.py
```

For mandatory hosted acceptance, first install the OpenType Sanitizer (`ots-sanitize`)
and Chromium (`python -m playwright install --with-deps chromium`), then use:

```sh
python tools/third_cohort/verify.py --require-ots --report docs/third-cohort-verification.json
python tools/third_cohort/browser_smoke.py --report docs/third-cohort-browser-verification.json
```

Build into an isolated directory, without touching checked-in fonts:

```sh
python tools/third_cohort/build.py --output /tmp/third-cohort-rebuild
```

`tools/third_cohort/specimen.py` emits **37** reproducible files: each family's
font-outline SVG specimen, full Unicode character map and standalone offline
HTML type tester, plus the cohort overview. The SVG lettering is drawn directly
from compiled TTF outlines—not by relying on a fallback font. The testers use
adjacent WOFF2, literal `textContent`, present a repertoire map and show missing
codepoint/font-load warnings. Size/leading/tracking/dark controls are functional.
They can be used via local file URLs or a loopback web server, no CDN necessary.

## Verification and acceptance

`verify.py` validates 14 groups: source codepoint set, nonempty geometry and bounds,
exact source-to-compiled integer contours and bearings, width/fixed-pitch/tabular
digit contract, style metadata, SHA-256 manifest binding, all-glyph FreeType
comparison, four handwritten master completeness, distinct final alphabets and
real lowercase, practical confusable-raster signatures, tileable light box/blocks,
treatment-specific regressions, two independent-process hash-seed rebuilds,
mandatory OpenType Sanitizer and retained report binding.

**9,144** paired FreeType comparisons (12 faces × 254 codepoints × 3 sizes: 18,
36 and 68px) check pixel and bearing equivalence between compiled TTF and decoded
WOFF2. These do not establish typographic usability or accessibility. Rebuilds
under Python hash seeds 17 and 991 must reproduce all **24 font exports and the
manifest byte-for-byte**. `specimen.py --check` rejects stale SVGs and HTML rather
than overwriting them. The hosted browser harness checks both loopback HTTP and
file-URL font loading, all 254 map cells, literal input, missing Unicode warnings,
controls/polarity/reset, visible failure on missing WOFF2, and absence of external
requests or script exceptions.

The one-time bootstrap workflow is used **only** to transfer checksummed source
text to a dedicated development branch, run hosted qualification, build binaries,
and commit them. Temporary transport files must disappear from the final tree.
A read-only regression workflow replaces it before PR review: `contents: read`,
no writes, no rebuilding over checked-in outputs, immutable evidence and clean
worktree checks. Squash merge prevents ephemeral source transport entering the
main-branch commit history. Exact-main verification runs once via normal push
triggers, never redundant CI just for benchmarking.

Retained reports in `docs/third-cohort-{manifest,verification,browser-verification}.json`
are SHA-bound to all 24 compiled files; old success is not evidence for a future
modified font. CI must be checked at the exact reviewed PR head. The final PR
records merger and exact-main evidence.

## Explicitly not accepted

No native Windows GDI/DirectWrite/ClearType installation trial, per-size pixel
hinting, physical printer/monitor trial, human-factors study, kerning program,
ligature shaping, variable-font axes, generalized combining-diacritic behavior,
non-Latin scripts, Powerline or Nerd Font expansions. Suggested size ranges
are creative trial contexts, not speed, comfort or dyslexia claims. Experimental
faces must not carry real alarms, safety-critical text, access credentials or
important serial-number transcription as the sole visual channel. Decorative
cutouts do not constitute certified physical stencil/fabrication toolpaths.

New fonts, original masters, new shared helpers, generated specimens and this
cohort's design documents use **SIL Open Font License 1.1**, no Reserved Font
Names, copied into every family. Earlier fonts/reference documents are
untouched and not relicensed by this publication.
