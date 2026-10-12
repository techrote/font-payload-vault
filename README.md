# font-payload-vault

techrote's font workshop: every custom font, its full source, and the rules for making the next one.

**If you are an AI agent asked to make, change or name a font: read this whole file first.** It is the brief, the house style
and the definition of done. The two companion documents are part of the brief:

- [`docs/rating-system.md`](docs/rating-system.md): request dials, delivery scoring, folder routing
- [`docs/naming-guide.md`](docs/naming-guide.md): textural/onomatopoeic naming rules and word banks

---

## 1. Repo map

| folder | holds | example |
|---|---|---|
| [`cmd-font-container/`](cmd-font-container/) | terminal, console and system-UI fonts | [`knurled-swarf/`](cmd-font-container/knurled-swarf/) |
| [`hot-font-box/`](hot-font-box/) | loud display and headline faces | |
| [`cachemonic/`](cachemonic/) | cursed, glitched, generative, deliberately broken experiments | |
| [`abandonware/`](abandonware/) | fonts the user soured on after use (moved here whole, never deleted) | |
| [`docs/`](docs/) | rating system, naming guide, historical idea dumps | |

Routing rules are in [rating-system.md → Routing](docs/rating-system.md#routing-which-folder-a-font-lands-in).
Each font lives in its own lowercase-hyphen folder inside one category folder.

## 2. Who you're working for

- **The user directs agents and judges results. They don't write code.** Explain choices as plain trade-offs (pros/cons, roughly
  "explain like I'm 13"). Never leave them a vague error to diagnose.
- **Windows first.** Fonts must install and render on Windows 10/11. Linux/web formats are bonuses.
- **Aesthetic:** industrial, down-to-earth, non-neon cyberpunk/ratrod. Function over form, but it should still look good after
  being dropped down the stairs and dragged through gravel.
- **Names:** textural or onomatopoeic adjectives, workshop nouns, **no colour names**. Obscure shop words are welcome.
- **Low friction:** when they need to do something, give a direct link (PR, artifact, file). When they must run commands,
  bundle them into one code block and put every warning *before* the block.
- **No licences on original work.** See [Licensing policy](#licensing-policy). This is deliberate; don't "fix" it.
- **Don't stop for questions you can answer yourself.** Ask only when a wrong guess would be expensive (big rebuilds, irreversible
  changes) *and* the request is genuinely ambiguous. Otherwise pick, state what you picked, and keep going.

### Licensing policy

Original work in this repo carries **no licence**: only a copyright line. This is a deliberate choice by the owner:

1. a quiet protest against copyright systems that are unfit for purpose today;
2. a spanner in automated "inspired generation" pipelines told to ignore licences: an unlicensed repo is an edge case they may not
   have been told how to handle;
3. anyone who genuinely wants to reuse something can reach out to techrote directly.

What that means for agents:

| situation | do |
|---|---|
| font drawn from scratch here (the default) | `Copyright (c) <year> techrote` only. **No** `LICENSE` file, **no** licence line in READMEs, **no** OpenType licence fields (name IDs 13/14), no SPDX tags, no "all rights reserved" boilerplate either |
| font derived from a **copyleft** source (SIL OFL, GPL with font exception, CC BY-SA) | inherit that licence exactly as it requires: ship its licence file, keep upstream copyright lines, fill name IDs 13/14, rename if there's a Reserved Font Name, credit the source in the README |
| font derived from a **permissive** source (MIT, Apache, public-domain bitmaps) | avoid if you can and draw it yourself instead. If you can't, keep whatever notices the source licence requires, and flag it in the PR so the owner decides |
| font derived from anything without a modification-permitting licence | don't |
| someone (or another agent) adds a licence to original work | remove it, unless the owner asked for it |

## 3. Workflow for a new font

1. **Read the request** and fill a [request sheet](docs/rating-system.md#request-sheet). Infer any blank dial from the job
   and say so in the PR.
2. **Pick a design approach** (section 4) and write down why in the font's `WORKFLOW.md`.
3. **Gather references, then draw.** Get the shapes right at the smallest/hardest size first; that's where fonts fail.
4. **Build with a script, never by hand in a GUI.** Every output must be reproducible from `source/` with one command.
5. **Verify** against the standards in section 5. Fix, rebuild, re-verify.
6. **Make specimens and look at them yourself** (render to PNG and inspect). Problems you can't see in numbers show up here.
7. **Name it** using the [naming procedure](docs/rating-system.md#naming-procedure-finished-fonts) and the naming guide.
8. **Document it:** README (user-facing) + WORKFLOW.md (agent-facing) + the filled delivery sheet.
9. **Branch, commit, push, give the user a one-click PR link.** Never push straight to `main`.
10. **Report honestly:** what was verified, what wasn't (e.g. "not tested inside Windows itself"), and one sensible next step.

## 4. Design approaches

Pick the approach that fits the job, not the one that's quickest to code.

### A. Hand-tuned multi-size bitmap (pixel fonts) — *the Knurled Swarf method*

Draw glyphs as text grids (`#` / `.`) at a few master sizes, derive in-between sizes by duplicating "quiet" rows/columns,
hand-fix what derivation gets wrong, then export bitmap strikes and pixel-square outlines.

- **Use for:** UI, terminal and system fonts at 6–16px; anything that must be razor-sharp on screen.
- **Pros:** pixel-perfect at every target size; plain-text source diffs nicely in git; fully scriptable.
- **Cons:** each size needs attention; curves are limited to what pixels allow; only crisp at target sizes and integer multiples.
- **Start from:** copy [`cmd-font-container/knurled-swarf/source/`](cmd-font-container/knurled-swarf/source/). The engine (`swarf.py`),
  exporter (`build.py`), verifier (`verify.py`) and tester are reusable. Replace the grid files and the `MASTER_SPECS` / `SIZES` tables.
  Read its [WORKFLOW.md](cmd-font-container/knurled-swarf/WORKFLOW.md) first.
- **Gotchas:** keep 1px stems 1px when deriving; never double a dot; keep symmetric glyphs symmetric; centre math symbols on the
  x-height; bold must widen 1px counters *before* smearing, or `m`/`w`/`M` clog.

### B. Single-grid pixel font (one design, integer scaling)

One grid (e.g. 5×7 or 8×16), exported so it's crisp at N, 2N, 3N…

- **Use for:** retro/terminal fonts used at one size or scaled in whole steps (games, HUDs, monospace terminals).
- **Pros:** fast; perfectly consistent; easy monospace.
- **Cons:** blurry at in-between sizes; one size has to suit every use.
- **Tip:** set units-per-em = grid height × 128 so every pixel edge lands on a whole font unit.

### C. Constructed / modular outline fonts

Build every glyph from a small kit of parts (straight segments, quarter arcs, fixed stroke widths) placed on a grid by code
(fontTools pens or a UFO pipeline), e.g. stencil, blueprint, DIN-like or engineering-drawing lettering.

- **Use for:** display and label fonts with an engineered, machined feel; fonts for laser cutting, CNC engraving, 3D-printed labels.
- **Pros:** scales cleanly; very consistent; changing one parameter changes the whole family.
- **Cons:** can look sterile; good curves and overshoots need care; needs real outline hygiene (section 5).
- **Tools:** `fontTools` (pens, `fontBuilder`), `ufoLib2` + `fontmake` for multi-master/variable builds, `skia-pathops` to remove overlaps.

### D. Stroke / skeleton fonts (monoline, plotter, engraving)

Define each glyph as centre-line paths, then expand with a pen shape (round, square, chisel) to a chosen width.

- **Use for:** monoline technical lettering; and single-line "engraving" fonts for CNC, laser, pen plotters (also ship the raw
  centre-lines as SVG/DXF/Hershey-style data, since engravers want the line, not the outline).
- **Pros:** one skeleton gives many weights and nib styles; natural fit for machining.
- **Cons:** joins and terminals need tuning; expanded outlines must be overlap-free.

### E. Segment / matrix displays

7/14/16-segment, dot-matrix, LED, VFD or nixie-style lettering generated from a segment map.

- **Use for:** HUDs, gauges, clocks, readouts, cyber-industrial dashboards.
- **Pros:** instantly readable as "machine"; tiny source; easy to make a matching segment-off "ghost" layer.
- **Cons:** some letters are compromises (k, m, w, x); not for running text.

### F. Distressed / procedural texture

Start from a clean base font (made here, or properly licensed) and apply deterministic erosion, pitting, chipping, spatter or
chatter, controlled by a fixed random seed.

- **Use for:** worn, ratrod, abandoned-machine looks; `cachemonic/` experiments.
- **Pros:** big personality from a small amount of design work.
- **Cons:** messy outlines (lots of points, needs cleanup); poor at small sizes; easy to overdo. Always keep the clean base too.
- **Rule:** the same seed must produce the same font, and the seed goes in WORKFLOW.md.

### G. Modifying an existing open font

Fork an open-licensed font (SIL OFL, Apache, public-domain bitmap fonts) and reshape it.

- **Use for:** when an existing skeleton is 80% there and the job is the last 20%.
- **Pros:** fastest route to broad character coverage and solid spacing.
- **Cons / musts:** respect the licence. OFL is copyleft: the derivative **stays OFL** (this is the main exception to the
  repo's no-licence policy). OFL fonts with a **Reserved Font Name** must be renamed, the licence file and
  copyright notice must ship with it, and the README must credit the source. Prefer copyleft or public-domain sources; see the
  [Licensing policy](#licensing-policy) for permissive ones. Never touch fonts whose licence doesn't allow
  modification. Proprietary system fonts (Tahoma, MS Sans Serif, Terminal, Fixedsys) are off-limits as sources: draw your own.

### H. Icon / symbol fonts

Glyphs for UI icons, status symbols or tray indicators, mapped to the Private Use Area (U+E000+) and/or ligatures.

- **Use for:** UI-mod projects that need crisp icons in the same rendering path as text.
- **Musts:** a `cheatsheet.md` listing every codepoint and its name; same vertical metrics as the companion text font.

### I. Variable fonts

One file with weight/width (or a custom "wear" axis) axes, built from masters with `fontmake`.

- **Use for:** outline families with several weights.
- **Cons:** not for pixel fonts (interpolation destroys the grid); some Windows apps only show the named instances.

### Choosing quickly

| job | approach |
|---|---|
| Windows UI / taskbar / menus, 6–16px | A |
| terminal / code font | A or B, monospace |
| big titles, posters, logos | C, D or F |
| CNC / laser / plotter lettering | D (+ single-line export) |
| gauges, HUDs, readouts | E |
| "make X but rougher" | F on top of A/C |
| icons in the UI-mod suite | H |

## 5. Standards for finished work (definition of done)

A font isn't finished until every applicable box is ticked. List any exceptions in the PR.

### Folder layout

```
<category>/<font-slug>/
  README.md          user-facing: what it is, which file to install, sizes, coverage, specimen images, delivery ratings sheet
  WORKFLOW.md        agent-facing: approach, pipeline, source format, how to edit and rebuild
  requirements.txt   pinned or minimum versions of every Python dependency
  .gitignore         previews, caches, __pycache__
  source/            everything needed to rebuild (grids/UFOs/scripts/templates); no generated files
  fonts/             generated outputs (committed, so the user can download without building)
  specimen/          PNG sheets + self-contained HTML type tester
```

### Build

- One command rebuilds every output from `source/` (document it in both READMEs).
- Deterministic: same source, same files. No timestamps that change per build (set `head.created`/`modified` explicitly).
- No manual GUI steps in the pipeline. Font editors are fine for sketching, but their output must be exported to source files the script reads.

### Formats

| format | required for |
|---|---|
| `.ttf` (installable, Regular + Bold at minimum unless the request says otherwise) | every font |
| `.woff2` | every font |
| per-size `.ttf` (`Family Npx`) | pixel fonts |
| TTF with embedded bitmap strikes (EBDT/EBLC) + `hdmx` | multi-size pixel fonts |
| `.fon` (Windows raster, cp1252) | pixel fonts, when "system"/GDI use is likely |
| `.bdf` | pixel fonts |
| `.otf` / variable `.ttf` | outline families where it adds value |
| single-line SVG/DXF | engraving/plotter fonts (approach D) |

### Metadata

- Name table: family (ID 1), style (ID 2), full name (ID 4), version (ID 5, `Version X.YYY`), PostScript name (ID 6, no spaces),
  typographic family/subfamily (IDs 16/17) when there are more than Regular/Bold/Italic/Bold Italic.
- Style linking: `fsSelection`, `macStyle` and `usWeightClass` agree, so Windows pairs Regular/Bold as one family.
- Copyright `Copyright (c) <year> techrote`. No licence fields, file or README line on original work; inherited copyleft
  licences only, per the [Licensing policy](#licensing-policy).
- Vertical metrics: `hhea`, `OS/2 typo` and `OS/2 win` agree; `USE_TYPO_METRICS` set; `winAscent`/`winDescent` cover every glyph,
  so Windows doesn't clip accents or box drawing.
- `achVendID` set, PANOSE family type set, Unicode and code page ranges recalculated.

### Character coverage (minimum)

- U+0020–U+007E (ASCII) and U+00A0–U+00FF (Latin-1), plus the cp1252 extras: `€ ‚ ƒ „ … † ‡ ‰ Š ‹ Œ Ž ‘ ’ “ ” • – — ™ š › œ ž Ÿ`
  (fill gaps where they make sense for the style; list any that are intentionally missing).
- A designed `.notdef` (hollow box), `space`, `nbsp`.
- Same coverage in every size and weight of a family.
- Terminal/system fonts: box drawing (single + double), block and shade elements, arrows.

### Verification (automate it in `verify.py`)

- **fontTools** loads and decompiles every table of every file.
- **OpenType Sanitizer** (`pip install opentype-sanitizer`) passes for every TTF/OTF/WOFF2. This is what browsers run.
- **FreeType render check:** render every glyph at its design sizes and compare with the source.
  - Pixel fonts: pixel-exact match (bitmap, bearings, advance) for every strike, every per-size outline and every FON face,
    and **zero grey pixels** when the outline is rendered anti-aliased at its native size.
  - Outline fonts: no open contours, consistent contour direction, no overlaps in static fonts (or removed with `skia-pathops`),
    no points outside the bounding box metrics, every glyph renders non-empty except spaces.
- **fontbakery** (`fontbakery check-universal`) for outline fonts: fix every FAIL, explain any WARN you keep.
- Kerning/spacing sanity: render `HH HO OO nn no oo` and a pangram at the main size; nothing collides or gaps.
- Expected verify output is documented (e.g. `ALL OK (112 checks)`).

### Specimens

- `specimen-sizes.png`: every size/weight, pangram + caps line, rendered from the real font data.
- `specimen-charset.png`: every glyph.
- An in-context mock (UI, poster, terminal, whatever the job is), so the user judges it where it'll live.
- `specimen.html`: self-contained type tester (fonts embedded as data URIs, works offline from disk, opens in Edge/Chrome).
- Look at every specimen yourself before shipping.

### Windows-specific checks

- Family names under 31 characters, including size and style suffixes.
- Raster `.fon` face named differently from the TrueType family (e.g. `… Sys`), so the two don't collide.
- Note in the README how display scaling (125%/150%) affects which size gets used.
- If you couldn't test inside Windows (cloud sessions can't), say so plainly and list what to check.

### Docs and hand-off

- README written for the user: which file to install, in a table, with plain language.
- WORKFLOW.md written for the next agent: enough to change one glyph and rebuild without reading the code.
- Delivery ratings sheet filled (requested vs achieved), with name runner-ups.
- Commit messages say what changed and why. Work on a `claude/…` branch; hand over a PR link.

## 6. Changing or retiring a font

- **Small fixes:** edit `source/`, rebuild, re-verify, bump the version (`1.000` → `1.001`), note it in the README changelog.
- **Renames:** rename family, files, folder and docs in one commit; rebuild; re-verify. Record the old name in the README.
- **Retiring:** when the user sours on a font, move its whole folder into `abandonware/` and add a row to that folder's README table (date + why).
  Don't delete anything.

## 7. Fonts in this repo

| font | folder | approach | sizes | status |
|---|---|---|---|---|
| Knurled Swarf | [`cmd-font-container/knurled-swarf/`](cmd-font-container/knurled-swarf/) | A | 6–16px, Regular + Bold | v1.000, verified; Windows-side install test pending |
